import threading
import gc
import shutil
import gzip
import zipfile
import os
from collections import OrderedDict
from datetime import datetime

#import time

import pandas as pd
from lxml import etree
from pymongo import MongoClient
import sqlite3
import logging
from logging.handlers import RotatingFileHandler

F_VERSION = "VERSION_AAM"
F_TECHNIQUE = "TECHNIQUE_AAM"
F_BTSTYPE = "BTSTYPE_AAM"
F_MONAME = "MONAME_AAM"
F_FILENAME = "FILENAME_AAM"
F_NENAME = "NENAME_AAM"
F_DATE = "AAMDATE"

class ParserXML(threading.Thread):
    VENDOR_HUW = "HUW"
    FILETYPE_XML = "xml"
    FILETYPE_UNKNOWN = -1
    FILETYPE_AUTOEXPORT = 2
    FILETYPE_AUTOBACKUP = 3
    FILETYPE_GEXPORT = 1
    NENAME_UNKNOWN = -1
    EXPORTDATE_UNKNOWN = -1
    NEVERSION_UNKOWN = [-1, -1, -1]
    NES_TO_IGNORE = ['DBS3900']  # we will not process these NEs as well (Like DCU etc.)
    currStatus = 0
    statusStr = "Idle"

    def __init__(self, name, CUSTOM_DATE_FILTER="", EXPORT_DB=True, EXPORT_CSV=True, INSERT_MONGO=False,
                 DUMPDIR="/home/aamhabiby/Desktop/resources/TEST/", EXPORT_DIR="/home/aamhabiby/Desktop/resources/",
                 isZip=False, merge_versions=False):
        super().__init__(name=name) #required as we are using a Thread class
        self.logger = self.setupLogger()
        self.CUSTOM_DATE_FILTER = CUSTOM_DATE_FILTER
        self.EXPORT_DB = EXPORT_DB
        self.INSERT_MONGO = INSERT_MONGO
        temp = datetime.now()
        self.EXPORT_DIR = os.path.join(EXPORT_DIR,
                                       "{:04d}{:02d}{:02d}_{:02d}{:02d}".format(temp.year,
                                                                                temp.month,
                                                                                temp.day,
                                                                                temp.hour,
                                                                                temp.minute))
        self.DUMPDIR = DUMPDIR
        self.statusStr = "Initialized"
        #self.loggerString = StringIO()
        self.progress = 0
        self.isZip = isZip #indicates if the DUMPDIR is a directory or just a zip file we need to extract
        self.merge_versions = merge_versions
        self.EXPORT_CSV = EXPORT_CSV
        self.logger.info("Initialized a new Parser object. Name of the thread is " + name)

    def status(self):
        self.logger.info("Returning current status as per called function.")
        return self.progress, \
               self.statusStr, \
               " Custom logs can be here.", \
               { "Custom Date Filter" : self.CUSTOM_DATE_FILTER,
                 "Export to DB" : self.EXPORT_DB,
                 "Insert to Mongo" : self.INSERT_MONGO,
                 "Directory of Dumps" : self.DUMPDIR,
                 "Export Directory" : self.EXPORT_DIR }

    def setupLogger(self):
        '''
        Just sets up the logger and returns the logger instance which was setup with the init function.

        :return: logger instance
        '''
        LOG_TAG = 'PARSER_XML'
        self.myLogger = logging.getLogger(LOG_TAG )
        self.myLogger.setLevel(logging.DEBUG)
        self.fh = RotatingFileHandler(LOG_TAG  + ".log", 'a', maxBytes=20*1024*1024,
                                      backupCount=20)
        self.fh.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        #self.sh = logging.StreamHandler()  #This is a stringIO based logger.
        #self.sh.setLevel(logging.INFO)
        #self.sh.setStream(self.loggerString)

        formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')
        self.ch.setFormatter(formatter)
        #self.sh.setFormatter(formatter)
        self.fh.setFormatter(formatter)

        self.myLogger.addHandler(self.ch)
        self.myLogger.addHandler(self.fh)
        #self.myLogger.addHandler(self.sh)
        return self.myLogger

    def getFileType(self, root, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
        # currently we know of two types of XML files
        # one is usually in GExport folder and used by PRS to get cell data
        # other is the xml in the NEXXXX directory for every NE in the network
        # There are differences in these file formats.
        # This function will try to determine the file type and return a string.
        # We should add more file types if we start supporting more XML formats.
        try:
            entries = 0
            ret = []
            if (vendor == self.VENDOR_HUW):
                if (filetype == self.FILETYPE_XML):
                    for a in root.iter():
                        entries = entries + 1
                        if entries >= 4:
                            break
                        ret.append([a.tag, a.attrib])
                    # print(len(ret[1][1]), ret[1])
                    # print(ret)
                    if (ret[0][0].lower() == "bulkcmconfigdatafile") and (ret[1][1] == ""):
                        return self.FILETYPE_GEXPORT
                    elif (str(ret[1][1].keys()).lower().find('fileformatversion') > -1):
                        # print(str(ret[1][1].keys()).lower().find('neversion'))
                        return self.FILETYPE_AUTOBACKUP
                    elif (str(ret[1][1].keys()).lower().find('neversion') > -1):
                        # print(str(ret[1][1].keys()).lower().find('neversion'))
                        return self.FILETYPE_AUTOEXPORT
                    else:
                        return self.FILETYPE_UNKNOWN
            else:
                return self.FILETYPE_UNKNOWN
        except Exception as e:
            self.logger.error("An exception occurred in the getFileType Function. " + str(e))
            return self.FILETYPE_UNKNOWN

    def getneversion(self, root, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
        try:
            ftype = self.getFileType(root, vendor, filetype)
            entries = 0
            ret_type = ""
            ret_technique = ""
            ret_version = ""
            if (ftype == self.FILETYPE_GEXPORT):
                for a in root.iter():
                    entries = entries + 1
                    if entries == 4:
                        if "name" in a.attrib.keys():
                            ret_type = a.attrib["name"]
                    elif entries == 5:
                        if "version" in a.attrib.keys():
                            sp_ver = a.attrib["version"].split(" ")
                            if (len(sp_ver) > 1):
                                ret_version = sp_ver[len(sp_ver) - 1]  # set version to the last string
                                ret_type = "".join(sp_ver[: len(
                                    sp_ver) - 1])  # the rettype will now be everything before last part of the version string
                                # if ret_type == "":
                                #    ret_type = sp_ver[0]
                                if "technique" in a.attrib.keys():
                                    ret_technique = a.attrib['technique']
                                else:
                                    ret_technique = ""
                            else:
                                ret_version = sp_ver[0]
                                if "technique" in a.attrib.keys():
                                    if ret_type == "":
                                        ret_type = a.attrib["technique"]
                                    ret_technique = a.attrib["technique"]
                                else:
                                    if ret_type == "":
                                        ret_type = "UNKNOWN"
                                    ret_technique = ""
                        return [ret_version.upper(), ret_technique.upper(), ret_type.upper()]
            elif (ftype == self.FILETYPE_AUTOEXPORT):
                for a in root.iter():
                    entries = entries + 1
                    if entries == 2:
                        assert a.tag.lower() == 'fileHeader'.lower()
                        for strVal in a.attrib.values():
                            strSpl = strVal.split(" ")
                            ret_type = strSpl[0]
                            ret_version = strSpl[len(
                                strSpl) - 1]  # take the last item as ret_version. (Example "BTS3900 LTE V100R015C500") we will keep BTS3900 and the V100R015C500
                            ret_technique = strVal
                            break
                        return [ret_version.upper(), ret_technique.upper(), ret_type.upper()]
            elif (ftype == self.FILETYPE_AUTOBACKUP):
                for a in root.iter():
                    entries = entries + 1
                    if entries == 2:
                        assert (a.tag.lower().find('fileHeader'.lower()) > -1)
                        # print(a.keys(), a.attrib)
                        for a_ch in a.attrib:
                            # print(a.attrib[a_ch])
                            if a_ch.lower().find('neversion') > -1:
                                strVal = a.attrib[a_ch]
                                ret_type = strVal.split(" ")[0]
                                # ret_version = strVal.split(" ")[1]
                                ret_version = strVal[len(ret_type) + 1:]  # include everything after first word
                                return [ret_version.upper(), ret_technique.upper(), ret_type.upper()]
            else:
                self.logger.info(
                    "The file type is not in the decision tree. Returning unknown NE version. " + str(ftype))
                return self.NEVERSION_UNKOWN
        except Exception as e:
            self.logger.error("Exception occurred in getneversion. " + str(e))
            return self.NEVERSION_UNKOWN

    def write_to_sqlite(self, df, newFileName, moname):
        try:
            conn = sqlite3.connect(newFileName)
            cur = conn.cursor()
            sql_TableName = moname
            for df_ColName, df_ColType in zip(df.columns.values, df.dtypes):
                currType = "TEXT"
                if "float" in str(df_ColType):
                    currType = "REAL"
                elif "int" in str(df_ColType):
                    currType = "INT"
                try:
                    q = "ALTER TABLE " + sql_TableName + " ADD COLUMN " + df_ColName + " " + currType
                    cur.execute(q)
                except Exception as e:
                    pass #the columns may exist already
                    #self.logger.info("Error while trying to add non-existent column " + str(e))
            try:
                df.to_sql(name=moname, con=conn, if_exists="append", index=False)
                conn.close()
                if self.EXPORT_CSV == True:
                    df.to_csv(os.path.join(os.path.split(newFileName)[0], moname + ".csv"), index=False, mode="a+")

            except ValueError as e:
                self.logger.error("Value Error occurred exporting " + moname + " to the database " + newFileName + ". " + str(e))
        except Exception as e:
            self.logger.error("Error occurred while trying to open a sqlite connection. " + str(e))


    def export_all_tables(self, root, exportdir, filename="", vendor=VENDOR_HUW, filetype=FILETYPE_XML):
        try:
            startRoot = root
            typeOfXML = self.getFileType(root, vendor=vendor, filetype=filetype)
            if typeOfXML == self.FILETYPE_GEXPORT:
                for i in root:
                    #print(i.tag, i.attrib)
                    if i.tag.lower() == 'configData'.lower():
                        for j in i:
                            #print(j.tag, j.attrib)
                            for k in j:
                                #print(k.tag, k.attrib)
                                startRoot = k
                                break
            elif typeOfXML == self.FILETYPE_AUTOEXPORT:
                startRoot = root

            elif typeOfXML == self.FILETYPE_AUTOBACKUP:
                self.export_autobackup_data(root=root, exportdir=exportdir, filename=filename,
                                            vendor=vendor,
                                            filetype=filetype)
                return

            else:
                self.logger.info("Unknown filetype. So not processing this file.")
                return

            CURRNENAME = self.get_ne_for_gexport(filename)
            CURRDATE = self.get_ne_datetime(root, filename)
            temp = self.getneversion(root, vendor=vendor, filetype=filetype)
            T_VERSION = temp[0]
            T_TECHNIQUE = temp[1]
            T_BTSTYPE = str(typeOfXML) + "-" + temp[
                2]  #this is so that in mongo db if we load all kinds of files, the collections are not duplicated

            for it in startRoot.iter():
                if (it.tag == 'class'):
                    currClass = it.attrib['name'].upper()
                    # print(currClass)
                    currTab = []
                    for obj in it.getchildren():
                        paramDict = dict()
                        for params in obj.getchildren():
                            # print(params.tag, params.attrib)
                            paramDict[params.attrib['name'].upper()] = params.attrib['value']
                        currTab.append(paramDict)

                    df = pd.DataFrame()
                    df = df.from_records(currTab)

                    if len(df) > 0:
                        df[F_VERSION] = T_VERSION
                        df[F_TECHNIQUE] = T_TECHNIQUE
                        df[F_BTSTYPE] = T_BTSTYPE
                        # This special processing is for GExport type files. The MO names in such files are like ACL_BSC6910UMTS so we only need ACL from this output
                        # moname = currClass.strip().replace(" ", "").replace(temp[2], "").replace("_", "")
                        moname = currClass.upper().split("_")
                        if len(moname) == 2:
                            if moname[0][: len(moname[1])] == moname[1]: #ALMCORRSHLD eNodeB
                                if len(moname[0][len(moname[1]):].strip()) > 0: #whatif it was ENODEB_ENODEB. 
                                    moname = moname[0][len(moname[1]):].strip()
                                else:
                                    moname = moname[0] #so we will keep to ENODEB
                            else:
                                moname = moname[0]  # so we will keep to ENODEB
                        else:
                            moname = currClass.strip().replace(" ", "").replace(temp[2], "").replace("_", "")

                        df[F_MONAME] = moname
                        df[F_FILENAME] = filename
                        df[F_NENAME] = CURRNENAME
                        df[F_DATE] = CURRDATE
                        CUSTOM_COL_COUNT = 7
                        cols = df.columns.tolist()  # we want to move the custom added 5 columns to the beginning of the frame
                        cols = cols[-CUSTOM_COL_COUNT:] + cols[:-CUSTOM_COL_COUNT]
                        df = df[cols]  # rearrange the columns so that custom columns are in the beginning
                        if self.EXPORT_DB == True:
                            if self.merge_versions == False: #If merge_versions is true then we will create single DB file for different versions but same Object like BTS3900 etc
                                newDir = os.path.join(exportdir, T_BTSTYPE, T_VERSION)
                            else:
                                newDir = os.path.join(exportdir, T_BTSTYPE)
                            newFileName = os.path.join(newDir, T_BTSTYPE + ".db")
                            if not os.path.exists(newDir):
                                try:
                                    os.makedirs(newDir)
                                except Exception as e:
                                    self.logger.error("Error while creating the export directory : " +
                                                      newDir + ". Function will now exit. " + str(e))
                                    return
                            self.write_to_sqlite(df=df, newFileName=newFileName, moname=moname)
                        if (self.INSERT_MONGO == True):
                            self.df_to_mongo(T_BTSTYPE, moname, df)
                    else:
                        pass

                    del (df)

        except Exception as e:
            self.logger.error("An Exception occurred in the main export_all_tables function. " + str(e))



    def normalize(self, name):
        if name[0] == "{":
            uri, tag = name[1:].split("}")
            return tag
        else:
            return name

    def get_ne_for_gexport(self, filename):
        '''
        Returns the NENAME, DATE, IP from the GExport file name
        :param filename:Full path to the GExport xml file
        :return:
        '''
        nename = "UNKNOWN"
        strSpl = os.path.split(filename)
        if len(strSpl) > 1:
            filePart = strSpl[1]
            if filePart.lower().find("gexport") > -1:  # this is the gexport dump
                # gexport naming is like "GExport_BSC01_IPADDRESS_TIMESTAMP.xml"
                totParts = filePart.split("_")
                nename = "_".join(totParts[1:len(totParts) - 2])
                return nename
            elif filePart.lower().find("all") > -1:  # this maybe of type ALL_LSI19191_123123.xml
                totParts = filePart.split("_")
                nename = "_".join(totParts[1:len(totParts) - 1])
        return nename


    def export_autobackup_data(self, root, exportdir,
                               filename, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
        # for i in root4.iter():
        #    if isinstance(i.tag, str):
        #        print(i.attrib, i.tag)
        #    else:
        #        print(i.text)
        try:
            NEVERSION = self.getneversion(root, vendor=vendor, filetype=filetype)
            # self.logger.info("NEVERSION = " + str(NEVERSION))
            if (NEVERSION == self.NEVERSION_UNKOWN):
                self.logger.info("NEVERSION is unknown so not processing this dump. ")
                return
            elif (NEVERSION[2] in self.NES_TO_IGNORE):  # we dont want to process these NEs
                self.logger.info("Ignoring this NE as BTSTYPE is in ignore list. (" + str(NEVERSION[2]) + ")")
                return
            NENAME = self.get_ne_name(root)
            NEDATE = self.get_ne_datetime(root, filename)
            if (NENAME == self.NENAME_UNKNOWN) or (NEDATE == self.EXPORTDATE_UNKNOWN):
                self.logger.error(
                    "NENAME or NEDATE is unknown (NENAME, NEDATE) = (" + str(NENAME) + ", " + str(NEDATE) + ")")
                return

            # tempDate = datetime.now()
            # tempDateFilter = "{:04d}-{:02d}-{:02d}".format(tempDate.year, tempDate.month, tempDate.day)
            # if (NEDATE.find(tempDateFilter) == -1) and (
            #        considerdateFilter == True):  # if this dump is not from today then dont process it
            #    self.logger.info("Not processing this dump as datefilter not matched (filter = " + tempDateFilter)
            #    return
            # elif considerdateFilter == False:
            #    tempDateFilter = self.CUSTOM_DATE_FILTER_FILE
            currClass = ""
            for child in root:
                # print(child.tag, " ==== " , child.attrib , " |||| \n")
                for grandchild in child:
                    # self.logger.info(normalize(grandchild.tag) + " = " + str(grandchild.attrib))
                    if (self.normalize(grandchild.tag).lower()) == 'class':
                        paramTab = []  # this will hold all parameters under this class MO
                        for a in grandchild.getchildren():
                            currClass = self.normalize(a.tag).upper()
                            for b in a.getchildren():
                                if self.normalize(b.tag).lower() == 'attributes':
                                    paramList = OrderedDict()  # start adding the parameters here
                                    for c in b.getchildren():
                                        if isinstance(c, etree._Comment):
                                            # print(c.text)
                                            if len(paramList) > 0:
                                                currPair = paramList.popitem()
                                                paramList[self.normalize(currPair[0])] = c.text.strip()
                                        else:
                                            paramList[self.normalize(c.tag).upper()] = c.text
                                            # print(normalize(currClass), normalize(c.tag), " = " , c.text)
                                    paramTab.append(paramList)
                                    # print("Appending here", paramList, currClass)
                            # print(paramList)
                        if (len(paramTab) > 0):
                            df = pd.DataFrame(paramTab)
                            if (len(df) > 0):
                                df[F_NENAME] = NENAME
                                df[F_MONAME] = currClass
                                df[F_VERSION] = NEVERSION[0]
                                df[F_TECHNIQUE] = NEVERSION[1]
                                df[F_BTSTYPE] = NEVERSION[2]
                                df[F_DATE] = NEDATE[:10]  # only the date part
                                df[F_FILENAME] = filename
                                CUSTOM_COL_COUNT = 7

                                cols = df.columns.tolist()  # we want to move the custom added columns to the beginning of the frame

                                cols = cols[-CUSTOM_COL_COUNT:] + cols[:-CUSTOM_COL_COUNT]
                                df = df[cols]

                                if (self.EXPORT_DB == True):
                                    if self.merge_versions == False:
                                        newDir = os.path.join(exportdir, NEVERSION[2], NEVERSION[0])
                                    else:
                                        newDir = os.path.join(exportdir, NEVERSION[2])
                                    newFileName = os.path.join(newDir,  NEVERSION[2] + ".db")
                                    if not os.path.exists(newDir):
                                        try:
                                            os.makedirs(newDir)
                                        except Exception as e:
                                            self.logger.error("Error while trying to create export directories. " +
                                                              newDir + ". Function will now exit. " + str(e))
                                            return
                                    self.write_to_sqlite(df=df, newFileName=newFileName,moname=currClass)
                                if (self.INSERT_MONGO == True):
                                    self.df_to_mongo(NEVERSION[2], currClass, df)
                            else:
                                pass

                            del (df)
                                # print("0 length class not exported.", currClass)
        except Exception as e:
            self.logger.error("An exception occurred in the export_autobackup_data function. " + str(e))

    def get_ne_name(self, root):
        retText = self.NENAME_UNKNOWN
        for temp in root.iter():
            if isinstance(temp, etree._Comment) == False:
                # print(normalize(temp.tag), temp.attrib)
                if self.normalize(temp.tag) == "NE":
                    # print(temp.tag, temp.attrib, temp.text)
                    for b in temp.getchildren():
                        if self.normalize(b.tag).lower() == "attributes":
                            for c in b.getchildren():
                                if self.normalize(c.tag) == "NENAME":
                                    retText = c.text
        if (retText == self.NENAME_UNKNOWN):
            self.logger.error("NENAME not found in the file while processing.")
        else:
            self.logger.info("NENAME found for this file is " + retText)
        return retText

    def get_ne_datetime(self, root, filename):
        retText = self.EXPORTDATE_UNKNOWN
        if self.getFileType(root) == self.FILETYPE_GEXPORT:
            strSpl = os.path.split(filename)
            if len(strSpl) > 1:
                filePart = strSpl[1]
                if filePart.lower().find("gexport") > -1:  # this is the gexport dump
                    # gexport naming is like "GExport_BSC01_IPADDRESS_TIMESTAMP.xml"
                    totParts = filePart.split("_")
                    lenParts = len(totParts)
                    retText = totParts[lenParts - 1][:8]
        elif self.getFileType(root) == self.FILETYPE_AUTOBACKUP or self.getFileType(root) == self.FILETYPE_AUTOEXPORT:
            for temp in root.iter():
                if isinstance(temp, etree._Comment) == False:
                    if self.normalize(temp.tag).lower().find("footer") > -1:
                        retText = temp.attrib['dateTime']
        retText = str(retText[:10]).replace("-", "")  # only return the Date part
        self.logger.info("NE Date found is : " + str(retText))
        return retText

    def run(self):
        try:
            tempDate = datetime.now()
            tempDateFilter = "{:04d}{:02d}{:02d}".format(tempDate.year, tempDate.month,
                                                         tempDate.day)  # this is to only extract the CFG xml files inside today's AUTOBAK folder

            MAIN_DIR = self.DUMPDIR

            # Not removing the export directory means, that in case of SQL DB, the files will be appended with new values.
            #try:
            #    self.logger.info("Trying to remove the export directory now.")
            #    shutil.rmtree(self.EXPORT_DIR)
            #except:
            #    self.logger.info("Export directory removal before actual export process failed.")

            if (self.isZip == True) or (os.path.split(self.DUMPDIR)[1].lower().find(".zip") > -1):
                #this seems to be a zip file so try to extract it
                self.logger.info("This seems to be a zip file (either by explicit option) or by the directory name split. Trying to unzip first.")
                try:
                    zr = zipfile.ZipFile(self.DUMPDIR, 'r')
                    extPath = os.path.join( os.path.split(self.DUMPDIR)[0] , "tmp")
                    if os.path.exists(extPath):
                        shutil.rmtree(extPath)
                    zr.extractall( extPath )
                    zr.close()
                    del(zr)
                    MAIN_DIR = extPath
                    self.logger.info("Extracted zip path is now : " + str(extPath))
                except Exception as e:
                    self.logger.error("An error ocurred while trying to extract dumpdir as a zip file. Exiting. " + str(e))
                    return


            if self.CUSTOM_DATE_FILTER.strip() != "":  # only for testing in order to add any xml file regardless of the date
                tempDateFilter = self.CUSTOM_DATE_FILTER
                self.logger.warning("Date filter is overridden. Will use this filter for directory. " + str(tempDateFilter))
            self.progress = 2

            totFiles = self.getListOfFiles(MAIN_DIR, dirFilter=tempDateFilter,
                                           fileFilter=tempDateFilter, extensionFilter=".gz",
                                           filterType="or") # We will scan only all .gz files
                                                            # matching the filters for date in directories

            totalFiles = len(totFiles)
            processedFiles = 0
            self.logger.info("Total files to be processed are : " + str(totalFiles))
            for singleFile in totFiles:
                f = self.un_gzip(singleFile)
                if os.path.isfile(f): #seems that the gunzip extraction was successful so follow the rabit
                    self.logger.info("Processing file number ({:03d}/{:03d})".format(processedFiles, totalFiles))
                    tree1 = etree.parse(f)
                    root1 = tree1.getroot()
                    self.export_all_tables(root=root1, exportdir=self.EXPORT_DIR, filename=f)
                    processedFiles += 1
                    self.progress = 100 * processedFiles / totalFiles
                    self.statusStr = "({:03d}/{:03d})".format(processedFiles, totalFiles)
                    try:
                        os.remove(f)
                    except Exception as e:
                        self.logger.error("Error removing the file : " + f + ". " + str(e))
                    del(tree1)
                    del(root1)
                    gc.collect()

            if (self.isZip == True) or (os.path.split(self.DUMPDIR)[1].lower().find(".zip") > -1):
                if os.path.exists(MAIN_DIR):
                    self.logger.info("Will now remove the processed directory as we believe it was a result of ZIP file extraction.")
                    try:
                        shutil.rmtree(MAIN_DIR)
                    except Exception as e:
                        self.logger.error("Unable to remove the directory created by zip process. " + str(e))
            self.progress = 100
            self.status = "Idle"
            self.logger.info("All files have been processed.")
            self.ch.close()
            self.fh.close()
            del (self.logger)
            gc.collect()
        except Exception as e:
            self.logger.error("An exception occurred while running the main run function. Exiting the thread now. "
                              "Please make sure the delete the uploaded files and extracted files before next operation.")

    def un_gzip(self, filename):
        try:
            input = gzip.GzipFile(filename, 'rb')
            s = input.read()
            input.close()
            output = open(filename[:-3], 'wb')
            output.write(s)
            output.close()
            self.logger.info("Extracted a gz file " + filename)
            del(input)
            del(s)
            del(output)
            return filename[:-3]
        except Exception as e:
            self.logger.info("Failure in gzip extraction of " + filename)
            return -1

    def df_to_mongo(self, dbname, collname, df, host="localhost", port=27017):
        try:
            client = MongoClient(host, port)
            db = client[dbname]
            collection = db[collname]
            data = df.to_dict(orient='records')
            collection.insert_many(data)
        except Exception as e:
            self.logger.error("Exception occurred inserting data to Mongo db" + str(e))

    def gunzip_all(self, dirName, dirFilter, fileFilter, extensionFilter, filterType="and"):
        try:
            self.logger.info(
                "The template for gunzip will be " + dirFilter + " and " + fileFilter + " and " + extensionFilter)
            for files in self.getListOfFiles(dirName=dirName, dirFilter=dirFilter,
                                             fileFilter=fileFilter, extensionFilter=extensionFilter,
                                             filterType=filterType):
                self.un_gzip(files)
        except Exception as e:
            self.logger.error("Exception occurred in gunzip_all function." + str(e))

    def getListOfFiles(self, dirName, dirFilter="", fileFilter="", extensionFilter=".xml", filterType="and"):
        # create a list of file and sub directories
        # names in the given directory
        try:
            listOfFile = os.listdir(dirName)
            allFiles = list()
            # Iterate over all the entries
            for entry in listOfFile:
                # Create full path
                fullPath = os.path.join(dirName, entry)
                # If entry is a directory then get the list of files in this directory
                if os.path.isdir(fullPath):
                    allFiles = allFiles + self.getListOfFiles(fullPath, dirFilter=dirFilter, fileFilter=fileFilter,
                                                              extensionFilter=extensionFilter, filterType=filterType)
                else:
                    # We will check for three conditions
                    # filename contains filefilter
                    # file extension matches the extension provided
                    # directory contains the directory filter
                    pathName, fileName = os.path.split(fullPath)
                    ffilt = 0
                    dfilt = 0
                    efilt = 0

                    if fileFilter != "":
                        if (fileName.lower().find(fileFilter.lower()) > -1):
                            ffilt = 1
                    else:
                        ffilt = 1
                    if dirFilter != "":
                        if (pathName.lower().find(dirFilter.lower()) > -1):
                            dfilt = 1
                    else:
                        dfilt = 1
                    if extensionFilter != "":
                        if (fileName[-len(extensionFilter):].lower() == extensionFilter.lower()):
                            efilt = 1
                    else:
                        efilt = 1

                    if filterType == "and":
                        if (ffilt == 1) and (dfilt == 1) and (efilt == 1):
                            allFiles.append(fullPath)
                    else:
                        if ( (ffilt == 1) or (dfilt == 1) ) and (efilt == 1):
                            allFiles.append(fullPath)

            return allFiles
        except Exception as e:
            self.logger.error("An error occurred while exploring the directories (getallfiles) " + str(e))
            return []

#To test the script, below can be used
#a = ParserXML(CUSTOM_DATE_FILTER="20190522", EXPORT_CSV=True, EXPORT_DB=True, merge_versions=True,
#              DUMPDIR="/media/windows/AAM/windows/Shared_Win_Ubuntu/lubuntu_backup/Desktop/resources/MIXEDSET.zip",
#              EXPORT_DIR="/home/aamhabiby/Desktop/resources/", name="parser_local")
#a.start()
#time.sleep(5)
#print(a.status())
#time.sleep(5)
#print(a.status())
