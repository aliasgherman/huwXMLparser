DUMPDIR = "/home/aamhabiby/Desktop/resources/TEST/"
EXPORT_DIR = "/home/aamhabiby/Desktop/resources/"
CONSIDER_DATEFILTERS = False
EXPORT_CSV = True
INSERT_MONGO = False
CUSTOM_DATE_FILTER_FILE = "2019-05-22"
CUSTOM_DATE_FILTER_DIR = "20190522"
#DUMPDIR = "E:\\AAM\\TEST"
#EXPORT_DIR = "E:\\AAM\\TEST"
#CONSIDER_DATEFILTERS = False



import pandas as pd
from lxml import etree
from collections import OrderedDict
from pymongo import MongoClient
import os
import gzip
from datetime import datetime
#import json

VENDOR_HUW = "HUW"
FILETYPE_XML = "xml"
FILETYPE_UNKNOWN = -1
FILETYPE_AUTOEXPORT = 2
FILETYPE_AUTOBACKUP = 3
FILETYPE_GEXPORT = 1
NENAME_UNKNOWN = -1
EXPORTDATE_UNKNOWN = -1
NEVERSION_UNKOWN = [-1, -1, -1]
NES_TO_IGNORE = ['DBS3900'] #we will not process these NEs as well (Like DCU etc.)

def getFileType(root, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    #currently we know of two types of XML files
    #one is usually in GExport folder and used by PRS to get cell data
    #other is the xml in the NEXXXX directory for every NE in the network
    #There are differences in these file formats.
    #This function will try to determine the file type and return a string.
    #We should add more file types if we start supporting more XML formats.
    try:
        entries = 0
        ret = []
        if (vendor == VENDOR_HUW):
            if (filetype == FILETYPE_XML):
                for a in root.iter():
                    entries = entries + 1
                    if entries >= 4:
                        break;
                    ret.append([a.tag, a.attrib])
                #print(len(ret[1][1]), ret[1])
                #print(ret)
                if (len(ret[1][1]) == 0):
                    #print(len(ret[1]))
                    return FILETYPE_GEXPORT
                elif (str(ret[1][1].keys()).lower().find('fileformatversion') > -1):
                    #print(str(ret[1][1].keys()).lower().find('neversion'))
                    return FILETYPE_AUTOBACKUP
                elif (str(ret[1][1].keys()).lower().find('neversion') > -1):
                    #print(str(ret[1][1].keys()).lower().find('neversion'))
                    return FILETYPE_AUTOEXPORT
                else:
                    return FILETYPE_UNKNOWN
        else:
            return FILETYPE_UNKNOWN
    except Exception as e:
        logger.error("An exception occurred in the getFileType Function. " + str(e))
        return FILETYPE_UNKNOWN

def getneversion(root, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    try:
        ftype = getFileType(root, logger, vendor, filetype)
        entries = 0
        ret_type = ""
        ret_technique = ""
        ret_version = ""
        if (ftype == FILETYPE_GEXPORT):
            for a in root.iter():
                entries = entries + 1
                if entries == 5:
                    ret_version = a.attrib['version'].split(" ")[1]
                    ret_type = a.attrib['version'].split(" ")[0]
                    ret_technique = a.attrib['technique']
                    #print(a.attrib)
                    return [ret_version, ret_technique, ret_type]
        elif (ftype == FILETYPE_AUTOEXPORT):
            for a in root.iter():
                entries = entries + 1
                if entries == 2:
                    assert a.tag.lower() == 'fileHeader'.lower()
                    for strVal in a.attrib.values():
                        ret_type = strVal.split(" ")[0]
                        ret_version = strVal[len(ret_type) + 1:] #include everything after first word
                        break
                    return [ret_version, ret_technique, ret_type]
        elif (ftype == FILETYPE_AUTOBACKUP):
            for a in root.iter():
                entries = entries + 1
                if entries == 2:
                    assert (a.tag.lower().find('fileHeader'.lower()) > -1)
                    #print(a.keys(), a.attrib)
                    for a_ch in a.attrib:
                        #print(a.attrib[a_ch])
                        if a_ch.lower().find('neversion') > -1:
                            strVal = a.attrib[a_ch]
                            ret_type = strVal.split(" ")[0]
                            #ret_version = strVal.split(" ")[1]
                            ret_version = strVal[len(ret_type) + 1:] #include everything after first word
                            return [ret_version, ret_technique, ret_type]
        else:
            logger.info("The file type is not in the decision tree. Returning unknown NE version. " + ftype)
            return [-1, -1, -1]
    except Exception as e:
        logger.error("Exception occurred in getneversion. " + str(e))
        return [-1, -1, -1]

def export_all_tables(root, exportdir, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    try:
        if getFileType(root,logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_GEXPORT:
            for i in root:
                print(i.tag, i.attrib)
                if i.tag.lower() == 'configData'.lower():
                    for j in i:
                        print(j.tag, j.attrib)
                        for k in j:
                            print(k.tag, k.attrib)
                            startRoot = k
                            break
        elif getFileType(root, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_AUTOEXPORT:
            startRoot = root

        elif getFileType(root, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_AUTOBACKUP:
            export_autobackup_data(root=root, exportdir=exportdir, logger=logger,considerdateFilter=CONSIDER_DATEFILTERS, vendor=VENDOR_HUW, filetype=FILETYPE_XML)
            return

        for it in startRoot.iter():
            if (it.tag == 'class'):
                currClass = it.attrib['name']
                #print(currClass)
                currTab = []
                for obj in it.getchildren():
                    paramDict = dict()
                    for params in obj.getchildren():
                        #print(params.tag, params.attrib)
                        paramDict[params.attrib['name']] = params.attrib['value']
                    currTab.append(paramDict)

                df = pd.DataFrame()
                df = df.from_records(currTab)
                df['MONAME'] = currClass
                temp = getneversion(root, logger)
                df['VERSION'] = temp[0]
                df['TECHNIQUE'] = temp[1]
                df['BTSTYPE'] = temp[2]
                if (len(df) > 0):
                    if EXPORT_CSV == True:
                        newFileName = os.path.join(exportdir, temp[2], currClass + ".csv")
                        if os.path.isfile(newFileName):
                            df.to_csv(newFileName, index=False, header=False, mode="a")
                        else:
                            newDir = os.path.join(exportdir, temp[2])
                            if not os.path.exists(newDir):
                                os.mkdir(newDir)
                            df.to_csv(newFileName, index=False) #use os to properly join the filenames for any OS
                else:
                    logger.info("0 length class not exported." + str(currClass))
    except Exception as e:
        logger.error("An Exception occurred in the main export_all_tables function. " + str(e))

def normalize(name):
    if name[0] == "{":
        uri, tag = name[1:].split("}")
        return tag
    else:
        return name


def export_autobackup_data(root, exportdir, logger, considerdateFilter=True,
                           vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    #for i in root4.iter():
    #    if isinstance(i.tag, str):
    #        print(i.attrib, i.tag)
    #    else:
    #        print(i.text)
    try:
        NEVERSION = getneversion(root, logger)
        #logger.info("NEVERSION = " + str(NEVERSION))
        if (NEVERSION == NEVERSION_UNKOWN):
            logger.info("NEVERSION is unknown so not processing this dump. ")
            return
        elif (NEVERSION[2] in NES_TO_IGNORE): #we dont want to process these NEs
            logger.info("Ignoring this NE as BTSTYPE is in ignore list. (" + str(NEVERSION[2]) + ")")
            return
        NENAME = get_ne_name(root, logger)
        NEDATE = get_ne_datetime(root, logger)
        if (NENAME == NENAME_UNKNOWN) or (NEDATE == EXPORTDATE_UNKNOWN):
            logger.error("NENAME or NEDATE is unknown (NENAME, NEDATE) = (" + str(NENAME) + ", " + str(NEDATE) + ")")
            return

        tempDate = datetime.now()
        tempDateFilter = "{:04d}-{:02d}-{:02d}".format(tempDate.year, tempDate.month, tempDate.day)
        if (NEDATE.find(tempDateFilter) == -1) and (considerdateFilter == True): #if this dump is not from today then dont process it
            logger.info("Not processing this dump as datefilter not matched (filter = " + tempDateFilter)
            return
        elif considerdateFilter == False:
            tempDateFilter = CUSTOM_DATE_FILTER_FILE
            
        for child in root:
            #print(child.tag, " ==== " , child.attrib , " |||| \n")
            for grandchild in child:
                #logger.info(normalize(grandchild.tag) + " = " + str(grandchild.attrib))
                if (normalize(grandchild.tag).lower()) == 'class':
                    paramTab = [] #this will hold all parameters under this class MO
                    for a in grandchild.getchildren():
                        currClass = normalize(a.tag)
                        for b in a.getchildren():
                            if normalize(b.tag).lower() == 'attributes':
                                paramList = OrderedDict()  #start adding the parameters here
                                for c in b.getchildren():
                                    if isinstance(c, etree._Comment):
                                        #print(c.text)
                                        if len(paramList) > 0:
                                            currPair = paramList.popitem()
                                            paramList[normalize(currPair[0])] = c.text
                                    else:
                                        paramList[normalize(c.tag)] = c.text
                                        #print(normalize(currClass), normalize(c.tag), " = " , c.text)
                                paramTab.append(paramList)
                                #print("Appending here", paramList, currClass)
                        #print(paramList)
                    if (len(paramTab) > 0):
                        df = pd.DataFrame(paramTab)
                        df['NENAME_AAM'] = NENAME
                        df['MONAME'] = currClass
                        df['VERSION'] = NEVERSION[0]
                        df['TECHNIQUE'] = NEVERSION[1]
                        df['BTSTYPE'] = NEVERSION[2]
                        df['AAMDATE'] = NEDATE
                        CUSTOM_COL_COUNT = 6

                        cols = df.columns.tolist() #we want to move the custom added 5 columns to the beginning of the frame

                        cols = cols[-CUSTOM_COL_COUNT:] + cols[:-CUSTOM_COL_COUNT]
                        df = df[cols]
                        if (len(df) > 0):
                            if (EXPORT_CSV == True):
                                newFileName = os.path.join(exportdir, NEVERSION[2], currClass + ".csv")
                                if os.path.isfile(newFileName):
                                    df.to_csv(newFileName, index=False, header=False, mode='a') #use os to properly join the filenames for any OS
                                else:
                                    newDir = os.path.join(exportdir, NEVERSION[2])
                                    if not os.path.exists(newDir):
                                        os.mkdir(newDir)
                                    df.to_csv(newFileName, index=False) #use os to properly join the filenames for any OS
                            if (INSERT_MONGO == True):
                                df_to_mongo(NEVERSION[2], currClass, df, logger)
                        else:
                            pass
                            #print("0 length class not exported.", currClass)
    except Exception as e:
        logger.error("An exception occurred in the export_autobackup_data function. " + str(e))

def get_ne_name(root, logger):
    retText = NENAME_UNKNOWN
    for temp in root.iter():
        if isinstance(temp, etree._Comment) == False:
            #print(normalize(temp.tag), temp.attrib)
            if normalize(temp.tag) == "NE":
                #print(temp.tag, temp.attrib, temp.text)
                for b in temp.getchildren():
                    if normalize(b.tag).lower() == "attributes":
                        for c in b.getchildren():
                            if normalize(c.tag) == "NENAME":
                                retText = c.text
    if (retText == NENAME_UNKNOWN):
        logger.error("NENAME not found in the file while processing.")
    else:
        logger.info("NENAME found for this file is " + retText)
    return retText

def get_ne_datetime(root, logger):
    retText = EXPORTDATE_UNKNOWN
    for temp in root.iter():
        if isinstance(temp, etree._Comment) == False:
            if normalize(temp.tag).lower().find("footer") > -1:
                retText = temp.attrib['dateTime']
    if (retText == EXPORTDATE_UNKNOWN):
        logger.error("NE Export date not found in the file while processing.")
    else:
        logger.info("NE Date found for this file is " + retText)
    return retText

def main(logger):
    tempDate = datetime.now()
    tempDateFilter = "{:04d}{:02d}{:02d}".format(tempDate.year, tempDate.month, tempDate.day) #this is to only extract the CFG xml files inside today's AUTOBAK folder    
    MAIN_DIR = DUMPDIR
    if CONSIDER_DATEFILTERS == False: #only for testing in order to add any xml file regardless of the date
        tempDateFilter = CUSTOM_DATE_FILTER_DIR
    gunzip_all(MAIN_DIR, logger, dirFilter=tempDateFilter, fileFilter="cfg",
              extensionFilter=".gz") #first gunzip all the gz files in all directories.
    totFiles = getListOfFiles(MAIN_DIR, logger, dirFilter=tempDateFilter, fileFilter="cfg", extensionFilter=".xml")
    logger.info("Total files to be processed are : " + str(len(totFiles)))
    for f in totFiles:
        tree1 = etree.parse(f)
        root1 = tree1.getroot()
        #print(getFileType(root1))
        #print(getneversion(root1))
        logger.info("Starting File " + f)
        export_all_tables(root=root1, exportdir=EXPORT_DIR, 
                          logger=logger)
    logger.info("All files have been processed.")

def un_gzip(filename, logger):
    try:
        input = gzip.GzipFile(filename, 'rb')
        s = input.read()
        input.close()
        output = open(filename[:-3], 'wb')
        output.write(s)
        output.close()
        logger.info("Extracted a gz file " + filename)
    except Exception as e:
        logger.info("Failure in gzip extraction of " + filename)        
        
def df_to_mongo(dbname, collname, df, logger, host="localhost", port=27017):
    try:
        client = MongoClient(host, port)
        db = client[dbname]
        collection = db[collname]
        data = df.to_dict(orient='records')
        collection.insert_many(data)
    except Exception as e:
        logger.error("Exception occurred inserting data to Mongo db" + str(e))

def gunzip_all(dirName, logger, dirFilter, fileFilter, extensionFilter):
    try:
        tempDate = datetime.now()
        tempDateFilter = "{:04d}{:02d}{:02d}".format(tempDate.year, tempDate.month, tempDate.day) #this is to only extract the CFG xml files inside today's AUTOBAK folder
        logger.info("The template for gunzip will be " + tempDateFilter)
        for files in getListOfFiles(dirName=dirName, logger=logger, dirFilter=dirFilter,
                                    fileFilter=fileFilter, extensionFilter = extensionFilter):
            un_gzip(files, logger)
    except Exception as e:
        logger.error("Exception occurred in gunzip_all function." + str(e))

def getListOfFiles(dirName, logger, dirFilter = "", fileFilter = "", extensionFilter = ".xml"):
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
            allFiles = allFiles + getListOfFiles(fullPath, logger, dirFilter, fileFilter, extensionFilter)
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
                
            if selecFilter == 3: # All three conditions met (or were not required)
                allFiles.append(fullPath)
    return allFiles
        
        
if __name__ == "__main__":
    ##########################################################
    import logging
    from logging.handlers import RotatingFileHandler
    LOG_TAG = 'HUW_XML_PARSER'

    myLogger = logging.getLogger(LOG_TAG)
    myLogger.setLevel(logging.DEBUG)

    fh = RotatingFileHandler(LOG_TAG + ".log", 'a', maxBytes=10*1024*1024, backupCount=20)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    myLogger.addHandler(ch)
    myLogger.addHandler(fh)
    ##########################################################
    
    main(myLogger)
    
fh.close() 
