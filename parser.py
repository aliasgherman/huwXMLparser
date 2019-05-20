import pandas as pd
from lxml import etree
from collections import OrderedDict

#import xml.etree.ElementTree as ET

file1 = '/media/windows/AAM/windows/NSN SA/Macros/CFGMMLProject/XMLFiles/GExport_@OS1746_Al-Dohayilat-Camp-Shahanya_10.134.0.100_20150908064903.xml'
file2 = '/media/windows/AAM/windows/NSN SA/Macros/CFGMMLProject/XMLFiles/ALL_NDS1847_MuaitherNSt_1556496754.xml'
file3 = '/media/windows/AAM/windows/NSN SA/Macros/CFGMMLProject/XMLFiles/AUTOBAKDATA20190517030456/CFGDATA.XML'


VENDOR_HUW = "HUW"
FILETYPE_XML = "xml"
FILETYPE_UNKNOWN = -1
FILETYPE_AUTOEXPORT = 2
FILETYPE_AUTOBACKUP = 3
FILETYPE_GEXPORT = 1
    
def getFileType(root, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    #currently we know of two types of XML files
    #one is usually in GExport folder and used by PRS to get cell data
    #other is the xml in the NEXXXX directory for every NE in the network
    #There are differences in these file formats.
    #This function will try to determine the file type and return a string.
    #We should add more file types if we start supporting more XML formats.
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

def getneversion(root, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    ftype = getFileType(root, vendor, filetype)
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
                    ret_version = strVal.split(" ")[1]
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
                        ret_version = strVal.split(" ")[1]
                        return [ret_version, ret_technique, ret_type]

def export_all_tables(root, exportdir, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    if getFileType(root,vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_GEXPORT:
        for i in root:
            print(i.tag, i.attrib)
            if i.tag.lower() == 'configData'.lower():
                for j in i:
                    print(j.tag, j.attrib)
                    for k in j:
                        print(k.tag, k.attrib)
                        startRoot = k
                        break
    elif getFileType(root,vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_AUTOEXPORT:
        startRoot = root
    
    elif getFileType(root,vendor=VENDOR_HUW, filetype=FILETYPE_XML) == FILETYPE_AUTOBACKUP:
        export_autobackup_data(root=root, exportdir=exportdir, logger=logger, 
                               vendor=VENDOR_HUW, filetype=FILETYPE_XML)
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
            temp = getneversion(root)
            df['VERSION'] = temp[0]
            df['TECHNIQUE'] = temp[1]
            df['BTSTYPE'] = temp[2]
            if (len(df) > 0):
                df.to_csv(exportdir + currClass + ".csv", index=False) #use os to properly join the filenames for any OS
            else:
                print("0 length class not exported.", currClass)

def normalize(name):
    if name[0] == "{":
        uri, tag = name[1:].split("}")
        return tag
    else:
        return name


def export_autobackup_data(root, exportdir, logger, vendor=VENDOR_HUW, filetype=FILETYPE_XML):
    #for i in root4.iter():
    #    if isinstance(i.tag, str):
    #        print(i.attrib, i.tag)
    #    else:
    #        print(i.text)
    NEVERSION = getneversion(root)
    for child in root:
        #print(child.tag, " ==== " , child.attrib , " |||| \n")
        for grandchild in child:
            logger.info(normalize(grandchild.tag) + " = " + str(grandchild.attrib))
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
                            print("Appending here", paramList, currClass)
                    #print(paramList)
                if (len(paramTab) > 0):
                    df = pd.DataFrame(paramTab)
                    df['MONAME'] = currClass
                    df['VERSION'] = NEVERSION[0]
                    df['TECHNIQUE'] = NEVERSION[1]
                    df['BTSTYPE'] = NEVERSION[2]
                    if (len(df) > 0):
                        df.to_csv(exportdir + currClass + ".csv", index=False) #use os to properly join the filenames for any OS
                    else:
                        print("0 length class not exported.", currClass)


def main(logger):
    tree1 = etree.parse(file3)
    root1 = tree1.getroot()
    print(getFileType(root1))
    print(getneversion(root1))
    export_all_tables(root=root1, exportdir="/home/aamhabiby/Desktop/resources/", 
                      logger=logger)
    

if __name__ == "__main__":
    ##########################################################
    import logging
    from logging.handlers import RotatingFileHandler
    LOG_TAG = 'HUW_XML_PARSER'

    myLogger = logging.getLogger(LOG_TAG)
    myLogger.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler(LOG_TAG + ".log", 'a', maxBytes=10*1024*1024, backupCount=20)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    myLogger.addHandler(ch)
    myLogger.addHandler(fh)
    ##########################################################
    
    main(myLogger)
    
    fh.close()        
