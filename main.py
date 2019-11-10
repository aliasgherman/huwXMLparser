import subprocess

import config as cfg
from datetime import datetime
from app.modules.xmldownloader import *
from app.modules.parserxml import *
from app.modules.mongotoexcel import *
from app.modules import parserxml_parallel

if cfg.DATE_TO_PROCESS == "":
    todayDate = datetime.now()
    todayDate = "{:04d}{:02d}{:02d}".format(todayDate.year, todayDate.month, todayDate.day)
else:
    todayDate = cfg.DATE_TO_PROCESS

HOST_LIST = cfg.HOST_LIST
LOCALFOLDER = cfg.LOCALFOLDER
EXPORT_PATH = os.path.join(cfg.EXPORT_PATH, todayDate)
ZIP_EXPORT_PATH = os.path.join(cfg.EXPORT_PATH, todayDate + ".7z")
FOL_LIST = cfg.FOL_LIST


if __name__ == "__main__":
    if cfg.DOWNLOAD_FILES_FROM_FTP == True:
        downloader = XMLDownloader(PATHFILTER=todayDate,
                                   HOST_LIST=cfg.HOST_LIST, FOL_LIST=cfg.FOL_LIST,
                                   LOCALFOLDER=cfg.LOCALFOLDER, type=cfg.DL_FILETYPE)
        downloader.run()


    if cfg.PARSE_FILES == True:
        logger = parserxml_parallel.setupLogger()
        ret_params = parserxml_parallel.initialize(logger=logger, CUSTOM_DATE_FILTER=todayDate,
                               EXPORT_DB=cfg.EXPORT_TO_SQLDB,
                               INSERT_MONGO=cfg.EXPORT_TO_MONGO,
                               DUMPDIR=cfg.LOCALFOLDER,
                               EXPORT_DIR=cfg.EXPORT_PATH,
                               merge_versions=cfg.MERGE_VERSIONS,
                               EXPORT_CSV=cfg.EXPORT_AS_CSV,
                               name="ParserXMLAuto")
        parserxml_parallel.run(logger=logger, ret_params=ret_params)
        # parserXML = ParserXML()
        # parserXML.start() #this is a thread so we will call start method (not run)


    if cfg.EXPORT_FILES_FROM_MONGO == True:
        exporter = MongoToExcel(DBNAME=cfg.EXPORT_FROM_DB, EXPORT_PATH=cfg.EXPORT_PATH,
                                TABLES_NEEDED=cfg.TABLES_TO_EXPORT, DATE_COLUMN="AAMDATE")
        exporter.run()
