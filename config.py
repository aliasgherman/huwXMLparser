SECRET_KEY = "0x910x900x89"
APPVERSION = "V2_1_1"
########################################################################################################################
# Configuration file for Globals
########################################################################################################################

DATE_TO_PROCESS = "20190522"  # If you want to use the latest DATES from the xml file to be processed automatically then
# set this to DATE_TO_PROCESS = ""

#LOCALFOLDER is the folder where you want to download the FTP files, where you want to read the XML files FROM.
LOCALFOLDER = "/media/windows/AAM/windows/Shared_Win_Ubuntu/lubuntu_backup/Desktop/resources/oMIXEDSET/"  # This is the folder where you want the files to be read from.

#EXPORT_PATH is the folder where you want to export the results from the parsing. Also the results from Mongo exports if any
EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"  # This is the path where you want to export the CSV files
# (If the CSV export option is enabled)

DL_FILETYPE = 2 #The file type to be downloaded. 1 Means Autobackup, 2 Means GExport, 3 Means the NE Folders inside GExport folder

# These are the steps you want to run in your automatic script setup.

#Step 1, DOWNLOAD_FILES_FROM_FTP : Set to True if you want to download the files from FTP as part of this script
DOWNLOAD_FILES_FROM_FTP = False  # If set to true, then we will attempt to download the files (AUTOBAKDATA files)

#Step 2, Set to True if you want your script to parse the xml files
PARSE_FILES = True  # If set to true then we will parse the files present in the LOCALFOLDER variable.
# All type of Huawei XML will be processed

#Step 3, Set to True if you want to export some tables from the Mongo DB database
EXPORT_FILES_FROM_MONGO = False  # If set to True, then we will attempt to export


########################################################################################################################
# Configuration for the Automatic downloader from FTP server
########################################################################################################################

#HOST_LIST contains a list of Server IP, Server Username, Server Password
HOST_LIST = [["10.200.163.7", "ftpuser", "PWD1"],
             # These are the FTP servers from where you want to download the AUTOBAK
             ["10.200.163.15", "ftpuser", "PWD2"],  # files
             ["10.200.163.230", "ftpuser", "PWD3"]]

#Usually dont need to be changed. These are the folders which will be downloaded from the FTP server.
# Add if you have different version and folders created on your server as well
FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS",
            "MICRO BTS3900"]  # These are the folder names on the FTP servers where you have the XML files.

########################################################################################################################
# Configuration for the XML Parser
########################################################################################################################


#Step 3, Set to True if you want your script to Export the results as a DB file which can be opened easily using
# SQL DB Explorer
EXPORT_TO_SQLDB = True
MERGE_VERSIONS = True #This will merge the different software versions into single file if Home object is the same. (
                      # like two RNCs with different versions will be combined in a single DB file and same CSV appended
EXPORT_AS_CSV = True # It will export CSV files IF AND ONLY IF the Export to SQLDB is also selected. CSV will be simply
                     # appended on one another so if for some reason the objects have different parameters
                     # then the file will be useless. SQL DB is still preferrable.
EXPORT_TO_MONGO = False  # It is preferred to load all files in Mongo as you can then perform Consistency checks,
# Parameter Change tracking etc etc

########################################################################################################################
# Configuration for the MongoDB to Excel Exporter
########################################################################################################################

TABLES_TO_EXPORT = ["TZ", "UCELL"]  # These tables should be exported from MOngo DB to an excel file
EXPORT_FROM_DB = "1-BTS3900"  # This is the database name from which we want to export the above tables
EXPORT_ALL_DATES = False  # Should we export all available dates in MOngo OR only the latest

########################################################################################################################