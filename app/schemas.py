from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Annotated, Optional


# Using pydantic to create schemas for our path operations 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 


# For generating user 


class GenerateUser(BaseModel):
    email: EmailStr
    password: str

class GeneratedResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


    class Config:
        from_attributes = True





# Response model 
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: GeneratedResponse

    class Config:
        from_attributes = True



class PostOut(BaseModel):
    Post: Post
    votes: int


# Creating schema for authenticating user login 

class Authenticate(BaseModel):
    email: EmailStr
    password: str



# Creating a schema for access token

class Token(BaseModel):
    access_token: str
    token_type: str


# Setting up a schema for our token data

class TokenData(BaseModel):
    id: Optional[int] = None


# Setting up our schema for voting 
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]