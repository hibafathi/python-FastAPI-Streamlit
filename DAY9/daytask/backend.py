from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"])

users = {}
sessions = {}


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/auth/register")
def register(user: UserRegister):
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(user.password)
    users[user.email] = hashed
    return {"message": "User registered successfully"}


@app.post("/auth/login")
def login(user: UserLogin):
    stored_hash = users.get(user.email)
    if stored_hash is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    sessions[token] = user.email
    return {"access_token": token, "token_type": "bearer"}