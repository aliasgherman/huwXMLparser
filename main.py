import subprocess

import config as cfg
from downloadAutobak import *
from exportToExcel import *
from loggersetup import *
from parserxml import *

if cfg.DATE_TO_PROCESS == "":
    todayDate = datetime.now()
    todayDate = "{:04d}{:02d}{:02d}".format(todayDate.year, todayDate.month, todayDate.day)
else:
    todayDate = cfg.DATE_TO_PROCESS

HOST_LIST = cfg.HOST_LIST
LOCALFOLDER = cfg.LOCALFOLDER
EXPORT_PATH = os.path.join(cfg.EXPORT_PATH, todayDate)
ZIP_EXPORT_PATH = os.path.join(cfg.ZIP_EXPORT_PATH, todayDate + ".7z")
FOL_LIST = cfg.FOL_LIST
finalCommand = r'"{}" a "{}" -r "{}" -mx=9'.format(cfg.loc_7z, ZIP_EXPORT_PATH, EXPORT_PATH)


if __name__ == "__main__":
    '''
    # Step 1 : Setup the logging (no print commands should be used in code.
    #           So that automatic scripts are easier to setup)
        # Logger parameters are 
        # TAG = A string for the logging file name and logging messages
        # MAX_FILE_SIZE = the max file size of the logging file after which it will be rotated
        # BACKUP_COUNT = number of previous logging files to keep
        # FILE_LOG_LEVEL = logging level of messages for the Log file
        # CONSOLE_LOG_LEVEL = logging level of messages for the stdout (CLI/Console)
    '''

    loggingClass = LoggerSetup(TAG="XML_PARSER", MAX_FILE_SIZE=1024 * 1024 * 20, BACKUP_COUNT=20,
                               FILE_LOG_LEVEL=logging.DEBUG, CONSOLE_LOG_LEVEL=logging.DEBUG)
    myLogger = loggingClass.run()

    '''
    # Step 2 : Download autobakup files
    # The autoback / GExport / NE export files are available on the FTP of U2020/U2000 servers.
    # This function can download the files for AUTOBACK which are generally available inside /ftproot/ folder
    # The parameters are
        # Logger : An instance of the logger setup in the step1
        # PATHFILTER : If you want to download files where the Path contains a specified string only then use this
        #               Example : PATHFILTER = "20190501" will only download files if the path contains this date
                        If blank then the files for TODAY's date will be downloaded only. This gives you the latest 
                        dumps every day
        # HOST_LIST : This is the configuration of your FTP servers and their username / passwords
                        Example : HOST_LIST = [ [10.1.1.1, "USER_FTP_1", "PWD_FTP_1"] ,
                                                [10.1.1.2, "USER_FTP_2", "PWD_FTP_2"] ]
                                                This means that you have configured two ftp servers (two U2020 export paths)
                                                Second field is Username and third is the password for that FTP server
        # FOL_LIST : Names of the folders to download. Usually they are similar to BTS3900, BTS5900, DBS3900 etc.
                    Example : FOL_LIST = ["BTS3900", "BTS5900"]
        # LOCALFOLDER : Path where the files should be downloaded on the local machine
        # type : Type of the file. For now it can only be XMLDownloader.AUTOBAK. Later versions should support GExport files
    '''

    if cfg.DOWNLOAD_FILES_FROM_FTP == True:
        downloader = XMLDownloader(myLogger, PATHFILTER=todayDate,
                                   HOST_LIST=HOST_LIST, FOL_LIST=FOL_LIST,
                                   LOCALFOLDER=LOCALFOLDER, type=XMLDownloader.AUTOBAK)
        downloader.run()

    '''
    # Step 3 : Parse the downloaded XML files and then export files to CSV or Import them to MongoDB or both
    # Parameters are 
        # logger : Instance of the logging function setup in step 1
        # CUSTOM_DATE_FILTER : If set to "" then we will only parse the files with today's date, else we will process
                                files for the date mentioned in this filter. 
                                Example : CUSTOM_DATE_FILTER = "" OR CUSTOM_DATE_FILTER = "20190522"
        # EXPORT_CSV : If set to True then this will export the MOs to CSV files
                        If the files were GExport type then the output folder will have name like 1-BTS3900
                        where 1 means Gexport type, 2 means NE files, No number means AUTOBAK files
                        This is just to prevent the case where all types of files for same Site are processed so that 
                        results are in different folder as file format are different for Gexport and autobak
        # INSERT_MONGO : If set to True then all parsed files will also be imported to Mongo DB
        # DUMPDIR : The location of the XML files. Can be any directory and we will search the subdirectories
        # EXPORT_DIR : If EXPORT_CSV is set to True then this is the folder where we should export the files
    '''

    if cfg.PARSE_FILES == True:
        parserXML = ParserXML(logger=myLogger, CUSTOM_DATE_FILTER=todayDate,
                              EXPORT_CSV=cfg.EXPORT_TO_CSV,
                              INSERT_MONGO=cfg.EXPORT_TO_MONGO,
                              DUMPDIR=LOCALFOLDER,
                              EXPORT_DIR=EXPORT_PATH)
        parserXML.run()
        if cfg.EXPORT_TO_CSV == True:
            myLogger.info(finalCommand)  # This is the command to combine the processed CSV files into a single 7z file
            subprocess.call(finalCommand, shell=True)

    '''
    # Optional Step: Utility to export tables from MongoDB. Any previous tables can be exported as Excel file
    # PLEASE NOTE THAT THE STEP2 and STEP3 are not required for this if the dumps are already in MongoDB
    # This gives easy access to previous dumps so that consistency checks / change audits can be performed
    # Parameters are
        #logger : Instance of logger setup in step1
        # DBNAME : Name of the database. This is equal to the BTSTYPE of the files processed
                        Example : BTS3900, BTS5900, Micro etc etc. 
                        You can check available DBs in mongodb by running a shell with Mongo in its path
                            Shell > mongo
                            mongo> show dbs;
                                *** Will list name of available databases
        #EXPORT_PATH : Folder where you want to export the excel sheet
        # TABLES_NEEDED : Names of the MO which you want to export in this excel. 
                        Example : TABLES_NEEDED = ["NE", "TZ", "CELLALGOSWITCH"]
        # DATE_COLUMN : For now just set it to "AAMDATE"
        # EXPORT_ALL_DATES : Should we export all entries or only export the latest dump
        # COLUMNS_TO_DROP : Just to drop the _id column in the result. Should not impact anything
        # TABLE_FOR_MAXDATE : We will use this table to check what is the Latest dump available for the Site
                            Example : TABLE_FOR_MAX_DATE = "NE" means that we will query the latest date available in
                                        "NE" Collection and then use that date to generate the output if 
                                        EXPORT_ALL_DATES is set to False. 

    '''

    if cfg.EXPORT_FILES_FROM_MONGO == True:
        exporter = MongoToExcel(logger=myLogger, DBNAME=cfg.EXPORT_FROM_DB, EXPORT_PATH=EXPORT_PATH,
                                TABLES_NEEDED=cfg.TABLES_TO_EXPORT, DATE_COLUMN="AAMDATE",
                                EXPORT_ALL_DATES=cfg.EXPORT_ALL_DATES,
                                COLUMNS_TO_DROP=['_id'], TABLE_FOR_MAXDATE="TZ")
        exporter.run()
