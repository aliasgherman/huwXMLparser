This set of scripts is used to export the 2G/3G/4G/5G Dumps from Huawei xml files
The XML files are exported by U2000/U2020 on the ftp paths automatically

There are three types of xml files supported for parsing the xml
1. AUTOBAK Files : These are usually placed at /ftproot/BTSTYPEXXX/Data folders
2. GExport XML : These are inside the /opt/oss/server/var/fileint/cm/GExport folders with the name like GExport_NENAME_IPADDRESS_TIMESTAMP.xml.gz
3. NE GExport XML : These are inside the /opt/oss/server/var/fileint/cm/GExport but are in Folders like NE1231. These folders contain files named like ALL_NENAME_TIMESTAMP.xml.gz

You can use any of these files for parsing or all of them together.

Dependencies : 

pip install pandas
pip install lxml
pip install pymongo

Usage :
Just go through the file named main.py and change the settings as per the comments mentioned

Broadly speaking there are 3 scripts and you can choose to run any OR all of them
++++ Step 1 is just setting up a logging function. So no need to do anything

1. Step 2 (Script to download autobak xml files) - This will download the autobak files if you have specified the FTP server IPs and user/pwd settings
If you dont need to download the files, then just comment out the lines under Step 2

2. Step 3 (Script for Actual Parsing of all valid xml files) - You just need to specify if you want to export results to CSV and if you also want to import results into Mongodb. Also specify where to export and import the files from.

3. Step 4 (This is just a helper utility to export tables from Mongo DB) - If you need some tables to be exported from MongoDB (if you had inserted the tables at anytime) then you can use this utility function. Just comment step 4 if not needed by you.

main.py

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

    downloader = XMLDownloader(myLogger, PATHFILTER=DATE_TO_PROCESS,
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

    parserXML = ParserXML(logger=myLogger, CUSTOM_DATE_FILTER=DATE_TO_PROCESS,
                          EXPORT_CSV=True,
                          INSERT_MONGO=False,
                          DUMPDIR=LOCALFOLDER,

                          EXPORT_DIR=EXPORT_PATH)
    parserXML.run()

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

    exporter = MongoToExcel(logger=myLogger, DBNAME="BTS3900", EXPORT_PATH=EXPORT_PATH,
                            TABLES_NEEDED=["NE"], DATE_COLUMN="AAMDATE", EXPORT_ALL_DATES=False,
                            COLUMNS_TO_DROP=['_id'], TABLE_FOR_MAXDATE="NE")
    exporter.run()
