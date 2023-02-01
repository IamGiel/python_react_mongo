from fastapi import APIRouter, Body, Request, HTTPException, status, Depends, Header
from typing import Union
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import User, SystemUser, TokenSchema
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm


# from replit import db
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from uuid import uuid4

from config.database import ATLAS

authroute = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"],
    responses={404: {"description": "Not found"}},
)

@authroute.get('/users', response_description="get users", response_model=List[User])
async def get_all_users(request: Request):
    list_of_users = list(ATLAS.instagram["users"].find(limit=100))
    print(f">>>>> list_of_users >>>>>> {list_of_users}")
    if list_of_users:
        return list_of_users
    else:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Cannot get list of users")

@authroute.post("/register", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def register_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    already_exist = ATLAS.instagram["users"].find_one(
        {"email":f'{user["email"]}'.lower()}
    )
    if already_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Account already exists!')
    
    if user["password"] != user["passwordConfirm"]:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password mismatch")
    
    # hash password
    user["password"] = get_hashed_password(user["password"])
    user["passwordConfirm"] = user["password"]
    user["verified"] = False
    user["created_at"] = f"{datetime.utcnow()}"
    user["updated_at"] = user["created_at"]
    
    
    new_user = ATLAS.instagram["users"].insert_one(user)
    created_user = ATLAS.instagram["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    
    if created_user:
        return created_user
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User is not created")

@authroute.post("/signin", response_description="Signin a new user", status_code=status.HTTP_201_CREATED, response_model=SystemUser)
async def sign_in_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = ATLAS.instagram['users'].find_one(
        {"email":form_data.username}
    )
    
    is_matching_password = verify_password(form_data.password, user["password"])
    print(f"form data {form_data}")
    print(f"user from ATLASDB {user}")
    if not is_matching_password:
        print(f"user is NOT authenticated!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Please check user credentials")

    print(f"user is authenticated!")
    return {
        "access_token": create_access_token(user['email'], timedelta(minutes=30)),
        "refresh_token": create_refresh_token(user['email'], timedelta(days=7)),
        "name":user["name"],
        "email":user["email"],
        "password":""
    }

@authroute.put("/user-account-by/{email}", response_description="Update a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def update_user_info(email:str, requests:Request, user_payload: User = Body(...), Authorize: AuthJWT = Depends()):
    access_token = Authorize.create_access_token(subject=user_payload["email"])
    # user_payload = jsonable_encoder(user_payload)
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    print(f"current user value: {current_user}")
    user_payload = {k: v for k, v in user_payload.dict().items() if v is not None}
    user_payload["updated_at"] = f"{datetime.utcnow()}"
    user_payload["password"] = get_hashed_password(user_payload["password"])
    user_payload["passwordConfirm"] = user_payload["password"]
    
    if len(user_payload) >= 1:
        update_user = ATLAS.instagram["users"].update_one(
            {"email":email}, {"$set":user_payload}
        )
        
        print(update_user.matched_count)
        
        if update_user.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")
    
    if (existing_user := ATLAS.instagram["users"].find_one({"email": email})) is not None:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"User details updated: \n {existing_user}")
        return existing_user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User test with email: {email} not found")
    print(f">>>>> user payload >>>>>> {user_payload}")
    return update_user

