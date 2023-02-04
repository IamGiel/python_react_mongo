from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from typing import Union
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import Post
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer

from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, get_current_user

from config.database import ATLAS
from bson.json_util import dumps

security = HTTPBearer()
 
postRoute = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@postRoute.get('/all-post', response_description="get posts")
async def get_all_posts(request: Request, current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
    list_of_posts =list(ATLAS.instagram["posts"].find({}, {'ObjectId': False}))
    print(f"current_user 🐍 {current_user}")
    print(f"list_of_users =======  {list_of_posts}")
    print(f"type list_of_posts {type(list_of_posts)}")
    if list_of_posts:
        return list_of_posts
    else:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Cannot get list of posts")
      
@postRoute.post('/create-post', response_description="get posts", response_model=Post)
async def create_post(post: Post, current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
  
  print(f"this is the submitted post of type POST\n {post}")

  user_ref = eval(current_user["userObj"])["email"]
  print(f"user_ref , checks user exists and gets the user email {user_ref}")
  
  valid_user = ATLAS.instagram["users"].find_one(
    {"email":user_ref}
  )
  print(f"valid_user, from user_ref, we get the - user details from mongodb  {valid_user}")
  
  if valid_user is not None:
    # insert
    post.postedBy = valid_user
    # remove password from the this calls returned response
    valid_user["password"] = None
    valid_user["passwordConfirm"] = None
    new_post =  ATLAS.instagram["posts"].insert_one(post.dict())
    created_post = ATLAS.instagram["posts"].find_one(
        {"_id": new_post.inserted_id}
    )
    return created_post
  else:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Failed to create post")
 
  
 
 
  # title:{
  #   type:String,
  #   required:true
  # },
  # description:{
  #   type:String,
  #   required:true
  # },
  # postedBy:{
  #   type:ObjectId,
  #   ref:'User'
  # },
  # imageURL:{
  #   type:String,
  #   default:'No photo yet'
  # },
  # imageTitle:{
  #   type:String,
  #   default:'No photo yet'
  # },
  # date:{
  #   type:String,
  #   required:true
  # },
  # assigned:{
  #   name:{
  #     type:String,
  #     required:true
  #   },
  #   value:{
  #     type:String,
  #     required:true
  #   },
  #   avatar:{
  #     type:String,
  #     required:true
  #   },
   
  # },
  # labelled:{
  #   name:{
  #     type:String,
  #     required:true
  #   },
  #   value:{
  #     type:String,
  #     required:true
  #   },
  # },
  # profilePic:{
  #   type:String,
  #   required:true
  # }