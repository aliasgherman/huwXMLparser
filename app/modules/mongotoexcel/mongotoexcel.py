import os

import pandas as pd
from pymongo import MongoClient
import logging
from logging.handlers import RotatingFileHandler

class MongoToExcel:
    def __init__(self, DBNAME, EXPORT_PATH, TABLES_NEEDED, DATE_COLUMN="AAMDATE",
                 DATEVALUE="",
                 MONGO_USER="", MONGO_PWD="", MONGO_PORT="localhost:27017"):
        self.C_DBNAME = DBNAME
        self.C_DATEPARAM = DATE_COLUMN  # the column which contains date of the table xml
        self.C_COLSTODROP = ['id']
        self.EXPORT_PATH = EXPORT_PATH
        self.TABLES_NEEDED = TABLES_NEEDED
        self.logger =self.setupLogger()
        self.DATEVALUE = DATEVALUE
        self.UNKNOWN_MAX_DATE = -1
        # mongodb://[username:password@]host1[:port1]
        if MONGO_USER.strip() != "" and MONGO_PWD.strip() != "":
            self.connStr = "mongodb://" + str(MONGO_USER) + ":" + str(MONGO_PWD) + "@" + str(MONGO_PORT) + "/"
        else:
            self.connStr = "mongodb://" + str(MONGO_PORT) + "/"
        if len(self.TABLES_NEEDED) == 0:
            self.TABLES_NEEDED = self.get_all_colls()

    def setupLogger(self):
        '''
        Just sets up the logger and returns the logger instance which was setup with the init function.

        :return: logger instance
        '''
        LOG_TAG = 'Mongo2Excel'
        self.myLogger = logging.getLogger(LOG_TAG )
        self.myLogger.setLevel(logging.DEBUG)
        self.fh = RotatingFileHandler(LOG_TAG  + ".log", 'a', maxBytes=20*1024*1024,
                                      backupCount=20)
        self.fh.setLevel(logging.INFO)
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        #self.sh = logging.StreamHandler()  #This is a stringIO based logger.
        #self.sh.setLevel(logging.INFO)
        #self.sh.setStream(self.loggerString)

        formatter = logging.Formatter('[ %(asctime)s ] [ %(name)s ][ %(levelname)s ] %(message)s')
        self.ch.setFormatter(formatter)
        #self.sh.setFormatter(formatter)
        self.fh.setFormatter(formatter)

        self.myLogger.addHandler(self.ch)
        self.myLogger.addHandler(self.fh)
        #self.myLogger.addHandler(self.sh)
        return self.myLogger


    def get_coll_as_table(self, COLLNAME):
        try:
            client = MongoClient(self.connStr)
            with client:
                db = client[self.C_DBNAME]
                coll = db[COLLNAME]
                MAXDATE = coll.find_one(sort=[(self.C_DATEPARAM, -1)])[self.C_DATEPARAM]
                if self.DATEVALUE == "":
                    return (pd.DataFrame(list(coll.find({self.C_DATEPARAM: MAXDATE}))).drop(self.C_COLSTODROP, axis=1))
                else:
                    return (pd.DataFrame(list(coll.find({self.C_DATEPARAM: self.DATEVALUE}))).drop(self.C_COLSTODROP, axis=1))
        except:
            self.logger.info(
                "Exception occurred during getting collection data. " + str(self.C_DBNAME) + ", " + str(COLLNAME) +
                ", " + str(self.C_DATEPARAM) + ", MAXDATE/DATEVAL = " + str(MAXDATE) + "/" + str(self.DATEVALUE))
            return pd.DataFrame()  # return an empty dataframe

    def get_all_colls(self):
        try:
            client = MongoClient(self.connStr)
            with client:
                db = client[self.C_DBNAME]
                coll = db.list_collection_names()
                self.logger.info("Got all collection names. Total = " + str(len(coll)))
                return coll
        except Exception as e:
            self.logger.info(
                "Exception occurred during getting all collection names. " + str(self.C_DBNAME) + ". " + str(e))
            return []

    def run(self):
        try:
            export_FILENAME = os.path.join(self.EXPORT_PATH, self.C_DBNAME + ".xlsx")
            if os.path.exists(self.EXPORT_PATH) == False:
                os.makedirs(self.EXPORT_PATH)
            sCount = 0
            if len(self.TABLES_NEEDED) == 0:
                self.TABLES_NEEDED = self.get_all_colls()
            with pd.ExcelWriter(export_FILENAME, engine='xlsxwriter',
                                options={'strings_to_numbers': True}) as writer:
                for tables in self.TABLES_NEEDED:
                    df = self.get_coll_as_table(tables)
                    if len(df) > 0:
                        df.to_excel(writer, sheet_name=str(sCount) + "_" + tables[:25], index=False)
                        sCount = sCount + 1
                    # "Sheetname should be less than 32 for excel
                    if (sCount % 10) == 0:
                        self.logger.info("Processed " + str(sCount) + " tables.")
            self.logger.info("All tables processed. " + str(sCount))
        except Exception as e:
            self.logger.error("An error occurred while trying to export tables from Mongo DB. " + str(e))


#exporter = MongoToExcel(logger=None, DBNAME="1-BTS3900", EXPORT_PATH="/home/aamhabiby/Desktop/resources/",
#                        TABLES_NEEDED=[], DATE_COLUMN="AAMDATE", DATEVALUE="20190522",
#                        COLUMNS_TO_DROP=['_id'])
#exporter.run()
