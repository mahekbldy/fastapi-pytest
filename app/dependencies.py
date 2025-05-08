from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List

from app.auth import decode_token
from app.models import load_users
from app.schemas import TokenData, UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Decode JWT to get the current user data."""
    return decode_token(token)


def get_filtered_users(id: int = None, name: str = None, role: str = None) -> List[UserOut]:
    """Get users filtered by id, name, or role."""
    users = load_users()

    if id:
        users = [user for user in users if user.id == id]
    if name:
        users = [user for user in users if name.lower() in user.name.lower()]
    if role:
        users = [user for user in users if role.lower() in user.role.lower()]

    return users
