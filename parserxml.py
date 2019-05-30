# DUMPDIR = "/home/aamhabiby/Desktop/resources/TEST/"
# EXPORT_DIR = "/home/aamhabiby/Desktop/resources/"
# CONSIDER_DATEFILTERS = False
# EXPORT_CSV = True
# INSERT_MONGO = False
# CUSTOM_DATE_FILTER_FILE = "2019-05-22"
# CUSTOM_DATE_FILTER_DIR = "20190522"
#DUMPDIR = "E:\\AAM\\TEST"
#EXPORT_DIR = "E:\\AAM\\TEST"
#CONSIDER_DATEFILTERS = False


import gzip
import os
from collections import OrderedDict
from datetime import datetime

import pandas as pd
from lxml import etree
from pymongo import MongoClient


class ParserXML:
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

    def __init__(self, logger, CUSTOM_DATE_FILTER="",
                 EXPORT_CSV=True, INSERT_MONGO=False,
                 DUMPDIR="/home/aamhabiby/Desktop/resources/TEST/",
                 EXPORT_DIR="/home/aamhabiby/Desktop/resources/"):
        self.logger = logger
        self.CUSTOM_DATE_FILTER = CUSTOM_DATE_FILTER
        self.EXPORT_CSV = EXPORT_CSV
        self.INSERT_MONGO = INSERT_MONGO
        self.EXPORT_DIR = EXPORT_DIR
        self.DUMPDIR = DUMPDIR

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

                    df['VERSION'] = T_VERSION
                    df['TECHNIQUE'] = T_TECHNIQUE
                    df['BTSTYPE'] = T_BTSTYPE
                    # This special processing is for GExport type files. The MO names in such files are like ACL_BSC6910UMTS so we only need ACL from this output
                    # moname = currClass.strip().replace(" ", "").replace(temp[2], "").replace("_", "")
                    moname = currClass.upper().split("_")
                    if len(moname) == 2:
                        if moname[0][: len(moname[1])] == moname[1]:
                            moname = moname[0][len(moname[1]):]
                        else:
                            moname = moname[0]
                    else:
                        moname = currClass.strip().replace(" ", "").replace(temp[2], "").replace("_", "")

                    df['MONAME'] = moname
                    df['FILENAME'] = filename
                    df['NENAME'] = CURRNENAME
                    CUSTOM_COL_COUNT = 6
                    cols = df.columns.tolist()  # we want to move the custom added 5 columns to the beginning of the frame
                    cols = cols[-CUSTOM_COL_COUNT:] + cols[:-CUSTOM_COL_COUNT]
                    df = df[cols]  # rearrange the columns so that custom columns are in the beginning

                    if len(df) > 0:
                        if self.EXPORT_CSV == True:
                            newDir = os.path.join(exportdir, T_BTSTYPE, T_VERSION)
                            newFileName = os.path.join(newDir, moname + ".csv")
                            if os.path.isfile(newFileName):
                                df.to_csv(newFileName, index=False, header=False, mode="a")
                            else:
                                if not os.path.exists(newDir):
                                    os.makedirs(newDir)
                                df.to_csv(newFileName, index=False)  # use os to properly join the filenames for any OS
                        if (self.INSERT_MONGO == True):
                            self.df_to_mongo(T_BTSTYPE, moname, df)
                    else:
                        pass
                        #self.logger.info("0 length class not exported." + str(moname))

        except Exception as e:
            self.logger.error("An Exception occurred in the main export_all_tables function. " + str(e))

    def normalize(self, name):
        if name[0] == "{":
            uri, tag = name[1:].split("}")
            return tag
        else:
            return name

    def get_ne_for_gexport(self, filename):
        strSpl = os.path.split(filename)
        if len(strSpl) > 1:
            filePart = strSpl[1]
            if filePart.lower().find("gexport") > -1:  # this is the gexport dump
                # gexport naming is like "GExport_BSC01_IPADDRESS_TIMESTAMP.xml"
                totParts = filePart.split("_")
                if len(totParts) < 4:
                    if (len(totParts) > 1):
                        return totParts[
                            1]  # does not seem to be the right format. So just return the second split string
                    else:
                        return "UNKNOWN"
                else:
                    return "_".join(totParts[1:len(totParts) - 2])  # return name excluding first item and last 2 items
            else:
                totParts = filePart.split("_")
                # this may be of the type ALL_NENAME_XX_XX_TIMESTAMP
                if (len(totParts) < 3):
                    if (len(totParts) > 1):
                        return totParts[1]
                    else:
                        return "UNKNOWN"
                else:
                    return "_".join(totParts[1:len(totParts) - 1])

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
            NEDATE = self.get_ne_datetime(root)
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
                            df['NENAME_AAM'] = NENAME
                            df['MONAME'] = currClass
                            df['VERSION'] = NEVERSION[0]
                            df['TECHNIQUE'] = NEVERSION[1]
                            df['BTSTYPE'] = NEVERSION[2]
                            df['AAMDATE'] = NEDATE[:10]  # only the date part
                            df['FILENAME'] = filename
                            CUSTOM_COL_COUNT = 7

                            cols = df.columns.tolist()  # we want to move the custom added 5 columns to the beginning of the frame

                            cols = cols[-CUSTOM_COL_COUNT:] + cols[:-CUSTOM_COL_COUNT]
                            df = df[cols]
                            if (len(df) > 0):
                                if (self.EXPORT_CSV == True):
                                    newDir = os.path.join(exportdir, NEVERSION[2], NEVERSION[0])
                                    newFileName = os.path.join(newDir, currClass + ".csv")
                                    if os.path.isfile(newFileName):
                                        df.to_csv(newFileName, index=False, header=False,
                                                  mode='a')  # use os to properly join the filenames for any OS
                                    else:
                                        if not os.path.exists(newDir):
                                            os.makedirs(newDir)
                                        df.to_csv(newFileName,
                                                  index=False)  # use os to properly join the filenames for any OS
                                if (self.INSERT_MONGO == True):
                                    self.df_to_mongo(NEVERSION[2], currClass, df)
                            else:
                                pass
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

    def get_ne_datetime(self, root):
        retText = self.EXPORTDATE_UNKNOWN
        for temp in root.iter():
            if isinstance(temp, etree._Comment) == False:
                if self.normalize(temp.tag).lower().find("footer") > -1:
                    retText = temp.attrib['dateTime']
        if (retText == self.EXPORTDATE_UNKNOWN):
            self.logger.error("NE Export date not found in the file while processing.")
        else:
            self.logger.info("NE Date found for this file is " + retText)
        return retText

    def run(self):
        tempDate = datetime.now()
        tempDateFilter = "{:04d}{:02d}{:02d}".format(tempDate.year, tempDate.month,
                                                     tempDate.day)  # this is to only extract the CFG xml files inside today's AUTOBAK folder
        MAIN_DIR = self.DUMPDIR
        if self.CUSTOM_DATE_FILTER.strip() != "":  # only for testing in order to add any xml file regardless of the date
            tempDateFilter = self.CUSTOM_DATE_FILTER
            self.logger.warn("Date filter is overridden. Will use this filter for directory. " + str(tempDateFilter))
        self.gunzip_all(MAIN_DIR, dirFilter=tempDateFilter, fileFilter="",
                        extensionFilter=".gz")  # first gunzip all the gz files in all directories.
        totFiles = self.getListOfFiles(MAIN_DIR, dirFilter=tempDateFilter, fileFilter="", extensionFilter=".xml")
        self.logger.info("Total files to be processed are : " + str(len(totFiles)))
        for f in totFiles:
            tree1 = etree.parse(f)
            root1 = tree1.getroot()
            # print(getFileType(root1))
            # print(getneversion(root1))
            self.logger.info("Starting File " + f)
            self.export_all_tables(root=root1, exportdir=self.EXPORT_DIR, filename=f)
        self.logger.info("All files have been processed.")

    def un_gzip(self, filename):
        try:
            input = gzip.GzipFile(filename, 'rb')
            s = input.read()
            input.close()
            output = open(filename[:-3], 'wb')
            output.write(s)
            output.close()
            self.logger.info("Extracted a gz file " + filename)
        except Exception as e:
            self.logger.info("Failure in gzip extraction of " + filename)

    def df_to_mongo(self, dbname, collname, df, host="localhost", port=27017):
        try:
            client = MongoClient(host, port)
            db = client[dbname]
            collection = db[collname]
            data = df.to_dict(orient='records')
            collection.insert_many(data)
        except Exception as e:
            self.logger.error("Exception occurred inserting data to Mongo db" + str(e))

    def gunzip_all(self, dirName, dirFilter, fileFilter, extensionFilter):
        try:
            tempDate = datetime.now()
            tempDateFilter = "{:04d}{:02d}{:02d}".format(tempDate.year, tempDate.month,
                                                         tempDate.day)  # this is to only extract the CFG xml files inside today's AUTOBAK folder
            self.logger.info(
                "The template for gunzip will be " + dirFilter + " and " + fileFilter + " and " + extensionFilter)
            for files in self.getListOfFiles(dirName=dirName, dirFilter=dirFilter,
                                             fileFilter=fileFilter, extensionFilter=extensionFilter):
                self.un_gzip(files)
        except Exception as e:
            self.logger.error("Exception occurred in gunzip_all function." + str(e))

    def getListOfFiles(self, dirName, dirFilter="", fileFilter="", extensionFilter=".xml"):
        # create a list of file and sub directories
        # names in the given directory
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath, dirFilter=dirFilter, fileFilter=fileFilter,
                                                          extensionFilter=extensionFilter)
            else:
                # We will check for three conditions
                # filename contains filefilter
                # file extension matches the extension provided
                # directory contains the directory filter
                pathName, fileName = os.path.split(fullPath)
                selecFilter = 0
                if fileFilter != "":
                    if (fileName.lower().find(fileFilter.lower()) > -1):
                        selecFilter = selecFilter + 1
                else:
                    selecFilter = selecFilter + 1
                if dirFilter != "":
                    if (pathName.lower().find(dirFilter.lower()) > -1):
                        selecFilter = selecFilter + 1
                else:
                    selecFilter = selecFilter + 1
                if extensionFilter != "":
                    if (fileName[-len(extensionFilter):].lower() == extensionFilter.lower()):
                        selecFilter = selecFilter + 1
                else:
                    selecFilter = selecFilter + 1

                if selecFilter == 3:  # All three conditions met (or were not required)
                    allFiles.append(fullPath)
        return allFiles
