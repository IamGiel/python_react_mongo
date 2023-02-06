from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Depends
from typing import Union
from fastapi.encoders import jsonable_encoder
from typing import List
from models.models import Post, User
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer

from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token, get_current_user

from config.database import ATLAS
from utils.utils import printOut

import json

security = HTTPBearer()

postRoute = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)



@postRoute.put('/edit-post/{_id}', description="Edit a post")
async def edit_post(_id: str, post_form: Post, current_user: User = Depends(get_current_user)):
    # make sure we get valid user
    user_ref:User = json.loads(current_user['userObj'])['user']
    print(f"current user email 📧 {user_ref['email']}")
    print(f"user_ref , checks user exists and gets the user email {user_ref['email']}")
    valid_user = ATLAS.instagram["users"].find_one(
        {"email": user_ref['email']}
    )
    is_admin = any('admin' in s for s in user_ref["roles"])
    print(f"is admin user ? {is_admin}")
     
    selected_post = ATLAS.instagram["posts"].find_one({"_id": ObjectId(_id)})
    # if current user is not owner of the post, dont allow an update
    if user_ref['email'] != selected_post["postedBy"]["email"] and is_admin == False:
      print(f"ITS NOT OK UPDATE EMAIL ❌❌❌")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User with email: {selected_post['_id']} cannot update this document")
    
     
      
    print(f"ITS OK TO UPDATE EMAIL ✅✅✅")
    selected_post["title"] = post_form.title
    selected_post["postedBy"] = valid_user
    selected_post["description"] = post_form.description
    selected_post["assigned"] = post_form.assigned.dict()
    selected_post["labelled"] = post_form.labelled.dict()
    selected_post["imageURL"] = post_form.imageURL
    selected_post["imageTitle"] = post_form.imageTitle
    selected_post["updated_at"] = f"{datetime.now().astimezone().isoformat()}"

    print(f"========================= {selected_post['_id']}")

    if selected_post is not None:
        newly_edited_post = ATLAS.instagram["posts"].update_one(
            {"_id": selected_post["_id"]}, {"$set": selected_post}
        )

    if newly_edited_post.matched_count == 0:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {selected_post['_id']} not found")
    
    if (existing_post := ATLAS.instagram["posts"].find_one({"_id": ObjectId(_id)})) is not None:
        id_to_print = None
        for labels in existing_post:
            print(labels)
            if labels == "_id":
                labels = f"{ObjectId(_id)}"
                id_to_print = labels
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"updated post with id {id_to_print}")

@postRoute.get('/all-post', response_description="get posts")
async def get_all_posts(request: Request, current_user: User = Depends(get_current_user), accesstoken=Depends(security)):
    list_of_posts = list(
        ATLAS.instagram["posts"].find({}, {'ObjectId': False}))
    print(f"current_user 😀 {current_user}")
    cur_user:User = json.loads(current_user['userObj'])['user']
    print(printOut(cur_user['roles']))
    if list_of_posts:
        return list_of_posts
    else:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="Cannot get list of posts")

@postRoute.post('/create-post', response_description="get posts", response_model=Post)
async def create_post(post: Post, current_user: int = Depends(get_current_user), accesstoken=Depends(security)):

    print(f"this is the submitted post of type POST\n {post}")
    user_ref:User = json.loads(current_user['userObj'])['user']
    print(f"user_ref , checks user exists and gets the user email {user_ref['email']}")

    valid_user = ATLAS.instagram["users"].find_one(
        {"email": user_ref['email']}
    )
    print(
        f"valid_user, from user_ref, we get the - user details from mongodb  {valid_user}")

    if valid_user is not None:
        # insert
        post.postedBy = valid_user
        post.created_at = f"{datetime.now().astimezone().isoformat()}"
        post.updated_at = f"{datetime.now().astimezone().isoformat()}"
        # remove password from the this calls returned response
        valid_user["password"] = None
        valid_user["passwordConfirm"] = None
        new_post = ATLAS.instagram["posts"].insert_one(post.dict())
        created_post = ATLAS.instagram["posts"].find_one(
            {"_id": new_post.inserted_id}
        )

        return created_post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Failed to create post")

@postRoute.delete('/delete-post-by-id/{_id}', response_description="Delete a post")
async def delete_a_post(_id:str, current_user:int = Depends(get_current_user), accesstoken=Depends(security)):
  delete_result = ATLAS.instagram["posts"].delete_one({"_id": ObjectId(_id)})

  if delete_result.deleted_count == 1:
    return f"Deleted a post with ID {_id}"


  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {_id} not found")


