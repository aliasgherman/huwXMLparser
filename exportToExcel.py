from datetime import datetime

import pandas as pd
from pymongo import MongoClient

EXPORT_PATH = "/home/aamhabiby/Desktop/resources/"

CURDATE = "{:04d}".format(datetime.now().year) + "{:02d}".format(datetime.now().month) + "{:02d}".format(datetime.now().day)

TABLES_NEEDED_5G = ["CAMGTCFG"]

C_DBNAME = 'BTS3900'
#C_COLLNAME = 'INTERFREQNCELL'
C_DATEPARAM = 'AAMDATE'
C_MAXDATE = ''
C_COLSTODROP = ['_id']


def get_max_date_from_tz(DBNAME, COLLNAME='TZ', MAXDATEPARAM="AAMDATE"):
    try:
        client = MongoClient('mongodb://localhost:27017/')
        with client:    
            db = client[DBNAME]
            coll = db[COLLNAME]
            MAXDATE = coll.find_one(sort=[(MAXDATEPARAM, -1)])[MAXDATEPARAM]
            return(MAXDATE)
    except:
        print("Exception occurred during getting max date", DBNAME, COLLNAME, MAXDATEPARAM)

def get_coll_as_table(DBNAME, COLLNAME, MAXDATEPARAM="AAMDATE"):
    try:
        client = MongoClient('mongodb://localhost:27017/')
        with client:    
            db = client[DBNAME]
            coll = db[COLLNAME]
            MAXDATE = coll.find_one(sort=[(MAXDATEPARAM, -1)])[MAXDATEPARAM]
            return(pd.DataFrame(list( coll.find({MAXDATEPARAM: MAXDATE}))).drop(C_COLSTODROP, axis=1))
    except:
        print("Exception occurred during getting collection data. ", DBNAME, COLLNAME, MAXDATEPARAM)
        return pd.DataFrame()  # return an empty dataframe
    

MAXDATETZ = get_max_date_from_tz(C_DBNAME)
export_FILENAME = EXPORT_PATH + "_5G.xlsx"
sCount = 0
with pd.ExcelWriter(export_FILENAME, engine='xlsxwriter',
                        options={'strings_to_numbers': True}) as writer:
    for tables in TABLES_NEEDED_5G:
        sCount = sCount + 1
        df = get_coll_as_table(C_DBNAME, tables, C_DATEPARAM)

        df.to_excel(writer, sheet_name=str(sCount) + "_" + tables[:25], index=False) #"Sheetname should be less than 32 for excel
        if (sCount % 10) == 0:
            print("Processed ", sCount," tables.")
	
