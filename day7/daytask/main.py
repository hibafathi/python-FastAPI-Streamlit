from fastapi import FastAPI
from database import init_db
from routers import tasks

app = FastAPI(
    title="Task Manager API",
    version="2.0.0"
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def home():
    return {"message": "Task API with SQLite is running"}