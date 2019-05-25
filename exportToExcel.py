import os

import pandas as pd
from pymongo import MongoClient


class MongoToExcel:
    def __init__(self, logger, DBNAME, EXPORT_PATH, TABLES_NEEDED, DATE_COLUMN, EXPORT_ALL_DATES, COLUMNS_TO_DROP,
                 TABLE_FOR_MAXDATE="NE"):
        self.C_DBNAME = DBNAME
        self.C_DATEPARAM = DATE_COLUMN  # the column which contains date of the table xml
        self.C_COLSTODROP = COLUMNS_TO_DROP
        self.C_MAXDATE = ""
        self.EXPORT_PATH = EXPORT_PATH
        self.TABLES_NEEDED = TABLES_NEEDED
        self.TABLE_FOR_MAXDATE = TABLE_FOR_MAXDATE
        self.logger = logger
        self.EXPORT_ALL_DATES = EXPORT_ALL_DATES
        self.UNKNOWN_MAX_DATE = -1

    def get_max_date_from_tz(self):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            with client:
                db = client[self.C_DBNAME]
                coll = db[self.TABLE_FOR_MAXDATE]
                MAXDATE = coll.find_one(sort=[(self.C_DATEPARAM, -1)])[self.C_DATEPARAM]
                return (MAXDATE)
        except:
            self.logger.error(
                "Exception occurred during getting max date " + str(self.C_DBNAME) + str(self.TABLE_FOR_MAXDATE) +
                str(self.C_DATEPARAM))
            return self.UNKNOWN_MAX_DATE

    def get_coll_as_table(self, COLLNAME, DATEVAL):
        try:
            client = MongoClient('mongodb://localhost:27017/')
            with client:
                db = client[self.C_DBNAME]
                coll = db[COLLNAME]
                if self.EXPORT_ALL_DATES == False:
                    return (pd.DataFrame(list(coll.find({self.C_DATEPARAM: DATEVAL}))).drop(self.C_COLSTODROP, axis=1))
                else:
                    return (pd.DataFrame(list(coll.find())).drop(self.C_COLSTODROP, axis=1))
        except:
            self.logger.info(
                "Exception occurred during getting collection data. " + str(self.C_DBNAME) + ", " + str(COLLNAME) +
                ", " + str(self.C_DATEPARAM) + ", " + str(DATEVAL))
            return pd.DataFrame()  # return an empty dataframe

    def run(self):
        MAXDATETZ = self.get_max_date_from_tz()
        export_FILENAME = os.path.join(self.EXPORT_PATH, self.C_DBNAME + ".xlsx")
        sCount = 0
        with pd.ExcelWriter(export_FILENAME, engine='xlsxwriter',
                            options={'strings_to_numbers': True}) as writer:
            for tables in self.TABLES_NEEDED:
                sCount = sCount + 1
                df = self.get_coll_as_table(tables, MAXDATETZ)

                df.to_excel(writer, sheet_name=str(sCount) + "_" + tables[:25], index=False)
                # "Sheetname should be less than 32 for excel
                if (sCount % 10) == 0:
                    self.logger.info("Processed " + str(sCount) + " tables.")
        self.logger.info("All tables processed. " + str(sCount))
