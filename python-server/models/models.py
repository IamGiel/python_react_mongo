import uuid
from typing import Optional, Any
from pydantic import BaseModel, Field, constr

from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


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
            
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    
class User(BaseModel):
    # _id: PydanticObjectId()
    name:str = Field(...)
    email:str = Field(...)
    password:str = Field(...)
    passwordConfirm: str = Field(...)
    imageUrl:str = Field(...)
    created_at:str = Field(...)
    updated_at:str = Field(...)
    verified: bool = False
    
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
                "verified":False
            }
        }
    
    
class UserOut(BaseModel):
    email: str = Field(..., description="email")
    name: str = Field(..., description="username")


class SystemUser(UserOut):
    password: str   




           
           
           
           
           
            
            
            