from fastapi import Header, HTTPException
from dotenv import load_dotenv
load_dotenv('./.env')
import os


jwt_secret_key =  os.environ.get('JWT_SECRET_KEY')

async def get_token_header(x_token: str = Header(), Authorization: str = Header()):
    if x_token != jwt_secret_key:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    if Authorization != jwt_secret_key:
        raise HTTPException(status_code=400, detail="Authorization Bearer header invalid")
    


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")