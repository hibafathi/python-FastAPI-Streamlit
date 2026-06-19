from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
import uuid

from database import (
    init_db,
    db_get_user_by_email,
    db_create_user,
    db_create_task,
    db_get_tasks_by_owner
)
from auth import get_current_user, sessions

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"])

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    priority: str = "low"

@app.on_event("startup")
def startup():
    init_db()

@app.post("/auth/register")
def register(user: UserRegister):
    existing = db_get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_context.hash(user.password)
    db_create_user(user.email, hashed)
    return {"message": "User registered successfully"}

@app.post("/auth/login")
def login(user: UserLogin):
    existing_user = db_get_user_by_email(user.email)
    if existing_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, existing_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = str(uuid.uuid4())
    sessions[token] = user.email
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks")
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    task_id = db_create_task(task.title, task.priority, current_user)
    return {"id": task_id, "title": task.title, "owner": current_user}

@app.get("/tasks")
def get_tasks(current_user: str = Depends(get_current_user)):
    return db_get_tasks_by_owner(current_user)