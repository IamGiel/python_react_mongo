from flask import Flask
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

from config.database import stopDB, startDB

import os
import pprint
import certifi

from routers.routes import router as book_router
from routers.authRoutes import authroute as userAuth_router


app = FastAPI()

@app.get("/")
async def root():
    return 'Hello world - Its Python! 🐍 '

@app.on_event("startup")
def startup_db_client():
    startDB()
    
@app.on_event("shutdown")
def shutdown_db_client():
    stopDB()
    
app.include_router(book_router)
app.include_router(userAuth_router)

