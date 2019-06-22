SECRET_KEY = "0x910x900x89"
APPVERSION = "V2_1_1"
########################################################################################################################
# Configuration file for constants
########################################################################################################################

DATE_TO_PROCESS = "20190522"  # If you want to use the latest DATES from the xml file to be processed automatically then
# set this to DATE_TO_PROCESS = ""

########################################################################################################################

HOST_LIST = [["10.200.163.7", "ftpuser", "PWD1"],
             # These are the FTP servers from where you want to download the AUTOBAK
             ["10.200.163.15", "ftpuser", "PWD2"],  # files
             ["10.200.163.230", "ftpuser", "PWD3"]]
########################################################################################################################

LOCALFOLDER = "/home/aamhabiby/Desktop/resources/MIXEDSET"  # This is the folder where you want the files to be read from.

EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"  # This is the path where you want to export the CSV files (If the CSV export option is enabled)

FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS",
            "MICRO BTS3900"]  # These are the folder names on the FTP servers where you have the XML files.

loc_7z = '7z'  # This is the command to run 7z. On a windows system this would be like "C:\\Program Files\\7z\\7z.exe" etc.

########################################################################################################################
########################################################################################################################
DOWNLOAD_FILES_FROM_FTP = False  # If set to true, then we will attempt to download the files (AUTOBAKDATA files)
PARSE_FILES = True  # If set to true then we will parse the files present in the LOCALFOLDER variable. All type of Huawei XML will be processed
EXPORT_TO_CSV = True  # CAUTION, if you have a lot of files in
# the LOCAL FOLDER For parsing then this option is PAINFULLY SLOW
# Only use this optino if the number of files to process is low.
########################################################################################################################
########################################################################################################################

EXPORT_TO_MONGO = False  # It is preferred to load all files in Mongo as you can then perform Consistency checks, Parameter Change tracking etc etc

EXPORT_FILES_FROM_MONGO = False  # If set to True, then we will attempt to export
# the selected tables from the Mongo DB into an Excel file
# The variabls are below

TABLES_TO_EXPORT = ["TZ", "UCELL"]  # These tables should be exported from MOngo DB to an excel file
EXPORT_FROM_DB = "1-BTS3900"  # This is the database name from which we want to export the above tables
EXPORT_ALL_DATES = False  # Should we export all available dates in MOngo OR only the latest

########################################################################################################################
