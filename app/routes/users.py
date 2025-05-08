from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

from app.schemas import UserOut
from app.models import load_users
from app.auth import decode_token
from app.dependencies import get_current_user

router = APIRouter()


@router.get("/", response_model=List[UserOut])
def list_users(
        id: Optional[int] = None,
        name: Optional[str] = None,
        role: Optional[str] = None,
        current_user: UserOut = Depends(get_current_user)
):
    users = load_users()

    # Apply filters
    if id:
        users = [user for user in users if user.id == id]
    if name:
        users = [user for user in users if name.lower() in user.name.lower()]
    if role:
        users = [user for user in users if role.lower() in user.role.lower()]

    return users
