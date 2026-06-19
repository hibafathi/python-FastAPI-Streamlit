from fastapi import APIRouter, HTTPException
from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import (
    db_get_all_tasks,
    db_get_task,
    db_create_task,
    db_update_task,
    db_partial_update,
    db_delete_task
)

router = APIRouter()

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(status: str = None):
    return db_get_all_tasks(status)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = db_get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    return db_create_task(task.model_dump())

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    if db_get_task(task_id) is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_update_task(task_id, task.model_dump())

@router.patch("/{task_id}", response_model=TaskResponse)
def partial_update(task_id: int, task: TaskUpdate):
    updates = {k: v for k, v in task.model_dump().items() if v is not None}
    result = db_partial_update(task_id, updates)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return result

@router.delete("/{task_id}")
def delete_task(task_id: int):
    if not db_delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted"}

@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int):
    task = db_get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_partial_update(task_id, {"completed": True})