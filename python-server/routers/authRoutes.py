from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, Header
from typing import Union
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import User, SystemUser, TokenSchema
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm

from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, get_current_user
from uuid import uuid4

from config.database import ATLAS
from bson.json_util import loads, dumps

authroute = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"],
    responses={404: {"description": "Not found"}},
)

@authroute.get('/users', response_description="get users", response_model=List[User])
async def get_all_users(request: Request, current_user: int = Depends(get_current_user)):
    list_of_users = list(ATLAS.instagram["users"].find(limit=100))
    print(f"current_user {current_user}")
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
async def sign_in_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = ATLAS.instagram['users'].find_one(
        {"email":form_data.username}
    )
    
    is_matching_password = verify_password(form_data.password, user["password"])
    print(f"form data {form_data}")
    print(f"user from ATLASDB {user}")
    if not is_matching_password:
        print(f"user is NOT authenticated!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Please check user credentials")

    print(f"user is authenticated! {user}")
    userdata = dumps(user)
    accTok =  create_access_token(data={"userObj":userdata})
    refTok = create_refresh_token(data={"userObj":userdata})
    # accTok =  create_access_token(data={"email":user['email']})
    # refTok = create_refresh_token(data={"email":user['email']})
    try:
        response.set_cookie('access_token',accTok)
        response.set_cookie('refresh_token',refTok)
        response.set_cookie('is_loggedin',True)
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{err}")
    else:

        return {
            "access_token": accTok,
            "refresh_token": refTok,
            "name":user["name"],
            "email":user["email"],
            "password":""
        }

@authroute.post("/refresh", response_description="Refresh token", status_code=status.HTTP_201_CREATED)
def refresh_token(response: Response,current_user: int = Depends(get_current_user), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        user_email = Authorize.get_jwt_subject()
        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = ATLAS.instagram["users"].find_one(
                {"email":f'{user_email}'.lower()}
            )
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        accTok =  create_access_token(user['email'], timedelta(minutes=30))
    
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
        
    response.set_cookie('access_token',accTok, timedelta(minutes=30))
    response.set_cookie('is_loggedin',True, timedelta(minutes=30))
    return {'access_token': accTok}


@authroute.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, current_user: int = Depends(get_current_user)):
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    response.set_cookie('is_loggedin', False, -1)
    return {'status': 'success'}

@authroute.put("/user-account-by/{email}", response_description="Update a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def update_user_info(email:str, current_user: int = Depends(get_current_user), user_payload: User = Body(...), Authorize: AuthJWT = Depends()):
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

