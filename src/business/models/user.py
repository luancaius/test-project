
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None = Field(default=None, gt=0)


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    age: int | None = Field(default=None, gt=0)


class UpdateUserRequest(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = Field(default=None, gt=0)

