from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

from app.schemas import User, TokenData
from app.models import load_users
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def authenticate_user(username: str, password: str) -> User | None:
    users = load_users()
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None


def create_access_token(user: User) -> str:
    payload = {
        "sub": str(user.id),
        "name": user.name,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(id=int(payload["sub"]), name=payload["name"], role=payload["role"])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
