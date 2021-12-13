from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import uuid4

from pydantic.fields import Field


class User(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    username: str
    email: EmailStr
    password: str
    fullName: Optional[str] = None
    disabled: Optional[bool] = None
    allowedModules: Optional[List[str]] = []


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    fullName: Optional[str]


class UpdateUser(BaseModel):
    fullName: Optional[str]
    email: Optional[str]
    password: Optional[str]
    allowedModules: Optional[List[str]]
