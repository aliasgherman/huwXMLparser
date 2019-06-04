# Configuration file for constants

DATE_TO_PROCESS = "20190522"
HOST_LIST = [["10.200.163.7", "ftpuser", "PWD1"],
             ["10.200.163.15", "ftpuser", "PWD2"],
             ["10.200.163.230", "ftpuser", "PWD3"]]

LOCALFOLDER = "/home/aamhabiby/Desktop/resources/MIXEDSET"

EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"

ZIP_EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"

FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS", "MICRO BTS3900"]

loc_7z = '7z'

loc_export = ZIP_EXPORT_PATH

DOWNLOAD_FILES_FROM_FTP = False  # If set to true, then we will attempt to download the files (AUTOBAKDATA files)

PARSE_FILES = True  # If set to true then we will parse the files present in the LOCALFOLDER variable. All type of Huawei XML will be processed
EXPORT_TO_CSV = True  # CAUTION, if you have a lot of files in
# the LOCAL FOLDER For parsing then this option is PAINFULLY SLOW
# Only use this optino if the number of files to process is low.
EXPORT_TO_MONGO = False  # It is preferred to load all files in Mongo as you can then perform Consistency checks, Parameter Change tracking etc etc

EXPORT_FILES_FROM_MONGO = False  # If set to True, then we will attempt to export
# the selected tables from the Mongo DB into an Excel file
# The variabls are below

TABLES_TO_EXPORT = ["TZ", "UCELL"]  # These tables should be exported from MOngo DB to an excel file
EXPORT_FROM_DB = "1-BTS3900"  # This is the database name from which we want to export the above tables
EXPORT_ALL_DATES = False  # Should we export all available dates in MOngo OR only the latest
