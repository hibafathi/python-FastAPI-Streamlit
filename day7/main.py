from fastapi import FastAPI
from pydantic import BaseModel
from database import init_db, add_task, get_tasks

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    priority: str = "low"

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/tasks")
def get_all_tasks():
    return get_tasks()

@app.post("/tasks")
def create_task(task: TaskCreate):
    return add_task(task.title, task.priority)