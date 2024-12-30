from pydantic import BaseModel, EmailStr

from datetime import datetime
from enum import Enum

class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str
    role : UserRoleEnum = UserRoleEnum.USER

class adminCreate(BaseModel):
    username : str
    password : str
    role : UserRoleEnum = UserRoleEnum.ADMIN

class UserLogin(BaseModel):
    username : str
    password : str

class UserResponse(BaseModel):
    id: int
    username : str
    email : str
    role : str
    created_at : datetime

class AdminResponse(BaseModel):
    id : int
    username: str
    role : str
    created_at : datetime

    class Config:
        orm_mode = True