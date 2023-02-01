from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

import os
import pprint
import certifi

load_dotenv('./.env')

MONGO_PASSWORD = os.environ.get("MONGO_PW")
DB_NAME = os.environ.get("DB_NAME")
ATLAS_URI2 = f"mongodb+srv://{DB_NAME}:{MONGO_PASSWORD}@cluster0.iy2o1qb.mongodb.net/?retryWrites=true&w=majority"
MONGO_CLIENT = MongoClient(ATLAS_URI2, tlsCAFile=certifi.where())
AUTH_SECRET = os.environ.get("JWT_SECRET_KEY")
ATLAS = type('', (), {})()

class Settings(BaseModel):
    authjwt_secret_key: str = AUTH_SECRET
    
    def startDB():
        db_lists = MONGO_CLIENT.list_database_names()
        database = MONGO_CLIENT[DB_NAME]
        collections = database.list_collection_names()
        ATLAS.instagram = database
        ATLAS.collections = collections
        # print(f"Connected to the MongoDB MONGO_CLIENT! {dir(app)}")
        print(f"Connected to the MongoDB! here are the db lists\n {db_lists}")
        # print(f"collections in this MONGO_CLIENTs are: \n{DB_COLLECTIONS}")
        # print(DATABASE)
        
    def stopDB():
        MONGO_CLIENT.close()

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

