from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, gt=0)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, gt=0)

