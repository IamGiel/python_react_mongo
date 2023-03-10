from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends, Header
from typing import Union
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import User, SystemUser, TokenSchema, Post, PostsOut
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, date, time, timezone
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer

from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, get_current_user
from uuid import uuid4

from config.database import ATLAS
from bson.json_util import loads, dumps

from bson.objectid import ObjectId
import pydantic
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

authroute = APIRouter(
    prefix="/user-auth",
    tags=["user-auth"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()

@authroute.get('/users', response_description="get users", response_model=List[User])
async def get_all_users(request: Request, current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
    list_of_users = list(ATLAS.instagram["users"].find(limit=100))
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
    user["created_at"] = f"{datetime.now().astimezone().isoformat()}"
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
async def sign_in_user(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = ATLAS.instagram['users'].find_one(
        {"email":form_data.username}
    )
    
    is_matching_password = verify_password(form_data.password, user["password"])
    if not is_matching_password:
        print(f"user is NOT authenticated!")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Please check user credentials")

    print(f"user is authenticated! ??? {user}")
    
    user["password"] = None
    user["passwordConfirm"] = None

    # username = dumps(user['email'])
    user_details = dumps({"user":user})
    accTok =  create_access_token(data={"userObj":user_details})
    refTok = create_refresh_token(data={"userObj":user_details})
    # accTok =  create_access_token(data={"email":user['email']})
    # refTok = create_refresh_token(data={"email":user['email']})
    response.set_cookie('access_token',accTok)
    response.set_cookie('refresh_token',refTok)
    response.set_cookie('is_loggedin',True)
    payload = {
        "access_token": accTok,
        "refresh_token": refTok,
        "name":user["name"],
        "email":user["email"],
        "password":"",
        "imageUrl":user["imageUrl"],
        "isLoggedin":True
    }
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=payload)
    # return {
    #     "access_token": accTok,
    #     "refresh_token": refTok,
    #     "name":user["name"],
    #     "email":user["email"],
    #     "password":""
    # }

@authroute.post("/refresh", response_description="Refresh token", status_code=status.HTTP_201_CREATED)
def refresh_token(response: Response,current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
    if current_user:
        accTok =  create_access_token(current_user)
        refTok =  create_refresh_token(current_user)
        response.set_cookie('access_token',accTok)
        response.set_cookie('refresh_token',refTok)
        response.set_cookie('is_loggedin',True)
        print("accTok: {accTok}")
        return {'access_token': accTok, 'refresh_token':refTok}
        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"token expired, please login again")
           
    


@authroute.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    response.set_cookie('is_loggedin', False, -1)
    payload = {
        "access_token": None,
        "refresh_token": None,
        "name":None,
        "email":None,
        "password":None,
        "imageUrl":None,
        "isLoggedin":False
    }
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=payload)

@authroute.put("/user-account-by/{email}", response_description="Update a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def update_user_info(email:str, current_user: int = Depends(get_current_user), user_payload: User = Body(...), accesstoken = Depends(security)):
    
    # username = dumps({"email":email})
    
    # access_token = create_access_token(data={"userObj":username})
    # print(f"current user value: {current_user}")
    user_payload = jsonable_encoder(user_payload)
    # user_payload = {k: v for k, v in user_payload.dict().items() if v is not None}
    user_payload["updated_at"] = f"{datetime.now().astimezone().isoformat()}"
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
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User test with email: {email} not found")
