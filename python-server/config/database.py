from pymongo import MongoClient
from dotenv import load_dotenv

import os
import pprint
import certifi

load_dotenv('./.env')
password = os.environ.get("MONGO_PW")
dbname = os.environ.get("DB_NAME")
ATLAS_URI2 = f"mongodb+srv://test:{password}@cluster0.iy2o1qb.mongodb.net/?retryWrites=true&w=majority"
mongoclient = MongoClient(ATLAS_URI2, tlsCAFile=certifi.where())

TEST_DB = type('', (), {})()

def startDB():
    db_lists = mongoclient.list_database_names()
    database = mongoclient.test
    collections = database.list_collection_names()
    TEST_DB.db = database
    TEST_DB.collections = collections
    # print(f"Connected to the MongoDB mongoclient! {dir(app)}")
    print(f"Connected to the MongoDB! here are the db lists\n {db_lists}")
    # print(f"collections in this mongoclients are: \n{DB_COLLECTIONS}")
    # print(DATABASE)
    
def stopDB():
    mongoclient.close()