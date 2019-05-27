from downloadAutobak import *
from parserxml import *
from exportToExcel import *


DATE_TO_PROCESS = ""
HOST_LIST = [["10.200.163.7", "ftpuser", "Vod_ftp_2015"],
             ["10.200.163.15", "ftpuser", "Vod_ftp_2015"],
             ["10.200.163.230", "ftpuser", "Changeme_123"]]

#LOCALFOLDER = "/home/aamhabiby/Desktop/resources/SMALLSET"
#EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"
# REMOTEFOLDER = "/ftproot/"
LOCALFOLDER = "E:/AAM/TEST"
EXPORT_PATH = "E:/AAM/TEST"
FOL_LIST = ["BTS3900", "BTS3900 LTE", "BTS5900 5G", "BTS5900 LTE", "PICO BTS3900", "DBS3900 IBS", "MICRO BTS3900"]


if __name__ == "__main__":
    ##########################################################
    # Setup the logger and then run the scripts
    ##########################################################
    import logging
    from logging.handlers import RotatingFileHandler

    LOG_TAG = 'HUW_XML_PARSER'

    myLogger = logging.getLogger(LOG_TAG)
    myLogger.setLevel(logging.DEBUG)

    fh = RotatingFileHandler(LOG_TAG + ".log", 'a', maxBytes=10 * 1024 * 1024, backupCount=20)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')

    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    myLogger.addHandler(ch)
    myLogger.addHandler(fh)
    ##########################################################
    # Logger has been setup
    ##########################################################

    ##########################################################
    # Step 1 : Download autobakup files
    ##########################################################
    #downloader = XMLDownloader(myLogger, PATHFILTER=DATE_TO_PROCESS, HOST_LIST=HOST_LIST, FOL_LIST=FOL_LIST, LOCALFOLDER=LOCALFOLDER, type=XMLDownloader.AUTOBAK)
    #downloader.run()

    ##########################################################
    # Step 2 : Parse the downloaded XML files : Optional this
    # step can also export all processed files as CSV
    ##########################################################
    parserXML = ParserXML(logger=myLogger, CUSTOM_DATE_FILTER=DATE_TO_PROCESS,
                       EXPORT_CSV=True,
                       INSERT_MONGO=False,
                       DUMPDIR=LOCALFOLDER,
                       EXPORT_DIR=LOCALFOLDER)
    parserXML.run()
    ##########################################################
    # Step 3 : Export the files from Mongo DB if they were
    # inserted in mongo in step 2
    ##########################################################

    exporter = MongoToExcel(logger=myLogger, DBNAME="BTS3900", EXPORT_PATH=EXPORT_PATH,
                            TABLES_NEEDED=["NE"], DATE_COLUMN="AAMDATE", EXPORT_ALL_DATES=False,
                            COLUMNS_TO_DROP=['_id'], TABLE_FOR_MAXDATE="NE")
    exporter.run()
    ##########################################################
    ##########################################################
    fh.close()
    ##########################################################
    ##########################################################
