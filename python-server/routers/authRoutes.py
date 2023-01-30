from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import UserOut, User
from datetime import datetime
from urllib.parse import unquote

# from replit import db
from utils.utils import get_hashed_password, verify_password
from uuid import uuid4

from config.database import TEST_DB

authroute = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"],
    responses={404: {"description": "Not found"}},
)

@authroute.get('/users', response_description="get users", response_model=List[User])
async def create_user(request: Request):
    list_of_users = list(TEST_DB.db["users"].find(limit=100))
    print(f">>>>> list_of_users >>>>>> {list_of_users}")
    if list_of_users:
        return list_of_users
    else:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Cannot get list of users")

@authroute.post("/register", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user_payload: User = Body(...)):
    user_payload = jsonable_encoder(user_payload)
    print(f">>>>> user payload >>>>>> {user_payload}")
    already_exist = TEST_DB.db["users"].find_one(
        {"email":f'{user_payload["email"]}'.lower()}
    )
    if already_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists!')
    
    if user_payload["password"] != user_payload["passwordConfirm"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password mismatch")
    
    # hash password
    user_payload["password"] = get_hashed_password(user_payload["password"])
    del user_payload["passwordConfirm"]
    user_payload["verified"] = True
    user_payload["created_at"] = f"{datetime.utcnow()}"
    user_payload["updated_at"] = user_payload["created_at"]
    
    
    new_user = TEST_DB.db["users"].insert_one(user_payload)
    created_user = TEST_DB.db["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    
    if created_user:
        return created_user
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User is not created")

@authroute.put("/user-account-by/{email}", response_description="Update a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def update_user(email:str, request: Request, user_payload: User = Body(...)):
    # user_payload = jsonable_encoder(user_payload)
    user_payload = {k: v for k, v in user_payload.dict().items() if v is not None}
    user_payload["updated_at"] = f"{datetime.utcnow()}"
    
    if len(user_payload) >= 1:
        update_user = TEST_DB.db["users"].update_one(
            {"email":email}, {"$set":user_payload}
        )
        print(update_user.matched_count)
        
        if update_user.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")
    
    if (existing_user := TEST_DB.db["users"].find_one({"email": email})) is not None:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"User details updated: \n {existing_user}")
        return existing_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User test with email: {email} not found")
    print(f">>>>> user payload >>>>>> {user_payload}")
    return update_user
