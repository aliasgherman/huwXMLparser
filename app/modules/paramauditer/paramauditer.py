import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

with client:
    db = client["BTS3900"]
    coll = db["ENODEBALGOSWITCH"]
    df = pd.DataFrame(list(coll.find()))

COLS_TO_IGNORE = ["AAMDATE", "BTSTYPE", "VERSION", "MONAME", "TECHNIQUE", "_id", "NENAME_AAM"]
df2 = df.drop(COLS_TO_IGNORE, axis=1)
df2 = df2.fillna(value=-9191)

df3 = df2.drop_duplicates(keep='first')
# df3 = df3.drop_duplicates(keep=False)
print("Non Duplicate rows are ", len(df3), " out of total rows ", len(df2))
