from fastapi import Header, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
sessions = {}

def get_current_user(authorization: str = Header(None)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = authorization.replace("Bearer ", "")
    email = sessions.get(token)
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return email