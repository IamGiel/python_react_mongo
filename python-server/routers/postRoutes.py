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

@postRoute.get('/all-posts', response_description="get posts")
async def get_all_posts(request: Request, current_user: int = Depends(get_current_user), accesstoken = Depends(security)):
  list_of_posts = list(ATLAS.instagram["posts"].find(limit=100))
  print(f"current_user {current_user}")
  if list_of_posts:
      return list_of_posts
  else:
      raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Cannot get list of posts")
 
 
 
 
 
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