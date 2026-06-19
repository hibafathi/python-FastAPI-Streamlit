from fastapi import APIRouter, HTTPException, Depends

from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import (
    db_create_task,
    db_get_tasks_by_owner,
    db_get_task_for_owner,
    db_update_task,
    db_delete_task
)
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    return db_create_task(task.model_dump(), current_user)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(current_user: str = Depends(get_current_user)):
    return db_get_tasks_by_owner(current_user)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: str = Depends(get_current_user)):
    task = db_get_task_for_owner(task_id, current_user)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: str = Depends(get_current_user)):
    if not db_delete_task(task_id, current_user):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted"}