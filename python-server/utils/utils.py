from datetime import datetime, timedelta
from typing import Union, Any
from dotenv import load_dotenv
import bcrypt
from fastapi import Depends
from jose import jwt
import os

load_dotenv('./.env')
salt = bcrypt.gensalt(12)

refresh_tok = os.environ.get("JWT_REFRESH_SECRET_KEY")
algo =  os.environ.get("ALGORITHM")
jwt_secret_key =  os.environ.get('JWT_SECRET_KEY')
acc_tok_exp_in_minutes =  os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES")

dbname = os.environ.get("DB_NAME")
# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("UTF-8"), salt)
    return hashed


def verify_password(password: str, hashed_pass: str) -> bool:
    is_match = bcrypt.checkpw(password.encode("UTF-8"), hashed_pass)
    if is_match:
        print(f'its matching password! 👍')
        
    else:
        print('oh no password dont match! 😔' )
        
    return is_match
    

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=refresh_tok)
        
        
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, refresh_tok, algo)
    print(f"encoded jwt {encoded_jwt}")
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=acc_tok_exp_in_minutes)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, refresh_tok, algo)
    return encoded_jwt