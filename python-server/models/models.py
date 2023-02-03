import uuid
import base64
from enum import Enum
from typing import Optional, Any, List
from pydantic import BaseModel, Field, constr
from uuid import UUID
from bson.objectid import ObjectId as BsonObjectId

class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    title: str = Field(...)
    author: str = Field(...)
    synopsis: str = Field(...)
    
    class Config:
            allow_population_field_name = True
            schema_extra = {
                "example": {
                    "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                    "title": "Don Quixote",
                    "author": "Miguel de Cervantes",
                    "synopsis": "..."
                }
            }
            
class BookUpdate(BaseModel):
    title:Optional[str]
    author:Optional[str]
    synopsis:Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Don Quixote",
                "author": "Miguel de Cervantes",
                "synopsis": "Don Quixote is a Spanish novel by Miguel de Cervantes..."
            }
        }   
  

class Roles(str, Enum):
    admin  = 'admin'
    user = 'user'
    other = 'other'
    not_given = 'not_given'
    
class User(BaseModel):
    name:str = Field(...)
    email:str = Field(...)
    password:str = Field(...)
    passwordConfirm: str = Field(...)
    imageUrl:str = Field(...)
    created_at:str = Field(...)
    updated_at:str = Field(...)
    verified: bool = False
    roles:Optional[List[Roles]] = None
    
    class Config:
        allow_population_field_name = True
        schema_extra = {
            "example": {
                # "_id": "1233-123333",
                "name":"Jo Jo Man",
                "email":"jj@mailer.com",
                "password":"123myman",
                "passwordConfirm":"123myman",
                "imageUrl":"http://myman.png",
                "created_at":"2023-01-28T23:21:08.799Z",
                "updated_at":"2023-01-28T23:21:08.799Z",
                "verified":False,
                "roles":["admin", "user"]
            }
        }
    
class UserOut(BaseModel):
    email: str = Field(..., description="email")
    name: Optional[str] = Field(..., description="username")

class SystemUser(UserOut):
    password: str
    access_token: Optional[str]
    refresh_token:Optional[str]
    
    class Config:
        allow_population_field_name = True
        schema_extra = {
            "example": {
                # "_id": "1233-123333",
                "name":"Jo Jo Man",
                "email":"jj@mailer.com",
                "password":"123myman",
                "access_token":"expireThistoken30minutes",
                "refresh_token":"expireThistoken7days"
            }
        }
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    

class UserOut2(BaseModel):
    id: UUID
    email: str


class SystemUser2(UserOut):
    password: str

# TESTING MODELS
class Labelled(BaseModel):
    name:str = Field(...)
    value:str = Field(...)
    avatar:str = Field(...)


class Assigned(Labelled):
    name:str = Field(...)
    value:str = Field(...)
    
class Post(BaseModel):
    title:str = Field(...)
    description:str = Field(...)
    postedBy: Optional[User]
    imageURL: str = Field(...)
    imageTitle: str = Field(...)
    date: str = Field(...)
    assigned:Optional[Assigned]
    labelled:Optional[Labelled]
    profilePic:str = Field(...)






           
           
           
           
           
            
            
            