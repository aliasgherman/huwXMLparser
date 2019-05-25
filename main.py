from exportToExcel import *
from parser import *

DATE_TO_PROCESS = "20190522"
DATE_TO_PROCESS_DIR = "2019-05-22"

if __name__ == "__main__":
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

    parser = ParserXML(logger=myLogger, CONSIDER_DATEFILTERS=False, CUSTOM_DATE_FILTER_FILE=DATE_TO_PROCESS_DIR,
                       CUSTOM_DATE_FILTER_DIR=DATE_TO_PROCESS,
                       EXPORT_CSV=False,
                       INSERT_MONGO=True,
                       DUMPDIR="/home/aamhabiby/Desktop/resources/SMALLSET/",
                       EXPORT_DIR="/home/aamhabiby/Desktop/resources/")
    parser.run()

    exporter = MongoToExcel(logger=myLogger, DBNAME="BTS3900", EXPORT_PATH="/home/aamhabiby/Desktop/resources/",
                            TABLES_NEEDED=["NE"], DATE_COLUMN="AAMDATE", EXPORT_ALL_DATES=False,
                            COLUMNS_TO_DROP=['_id'], TABLE_FOR_MAXDATE="NE")
    exporter.run()

    fh.close()
