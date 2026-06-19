from fastapi import APIRouter, HTTPException, Depends
import uuid

from schemas import UserRegister, UserLogin, UserResponse
from database import db_get_user_by_email, db_create_user
from auth import pwd_context, sessions, get_current_user

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    existing = db_get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(user.password)
    db_create_user(user.email, hashed)
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    existing_user = db_get_user_by_email(user.email)
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, existing_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    sessions[token] = user.email
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: str = Depends(get_current_user)):
    user = db_get_user_by_email(current_user)
    return {"id": user["id"], "email": user["email"]}