from pydantic import BaseModel
from typing import Optional


# Input Schema for Login (used by OAuth2PasswordRequestForm so not needed explicitly)

# Token Schema for Login Response
class Token(BaseModel):
    access_token: str
    token_type: str


# Token Payload (Data encoded in JWT)
class TokenData(BaseModel):
    id: int
    name: str
    role: str


# Internal User structure from JSON
class User(BaseModel):
    id: int
    username: str
    password: str  # stored as plain-text here, only for demonstration!
    name: str
    role: str


# Response Model - public-safe user info
class UserOut(BaseModel):
    id: int
    name: str
    role: str
