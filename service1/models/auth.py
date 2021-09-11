from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    name: str
    level: int
    token: str
    password: str
    email: str
    reg_time: float
    payment_method: Optional[str]


class LoginUserModel(BaseModel):
    email: str
    password: str


class AddUserModel(BaseModel):
    email: str
    name: str
    level: int
    password: str


class AddUserRequest(BaseModel):
    user: AddUserModel
    token: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str
    message: Optional[str]
