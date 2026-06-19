from pydantic import BaseModel, ValidationError
from typing import Dict, List
class TaskNotFoundError(Exception):
    pass
class Task(BaseModel):
    id: int
    title: str
    priority: str = "low"
    completed: bool = False

tasks: Dict[int, dict] = {}

def get_all_tasks() -> List[dict]:
    return list(tasks.values())


def get_task(task_id: int) -> dict:
    if task_id not in tasks:
        raise TaskNotFoundError(f"Task {task_id} not found")
    return tasks[task_id]


def create_task(data: dict) -> dict:
    task = Task(**data)

    if task.id in tasks:
        raise ValueError("Task ID already exists")

    tasks[task.id] = task.model_dump()
    return tasks[task.id]


def update_task(task_id: int, data: dict) -> dict:
    if task_id not in tasks:
        raise TaskNotFoundError(f"Task {task_id} not found")

    updated_data = {**tasks[task_id], **data}

    task = Task(**updated_data)

    tasks[task_id] = task.model_dump()
    return tasks[task_id]


def delete_task(task_id: int) -> bool:
    if task_id not in tasks:
        raise TaskNotFoundError(f"Task {task_id} not found")

    del tasks[task_id]
    return True
def menu() -> None:
    while True:
        print("\nTASK MANAGER ")
        print("1. Create Task")
        print("2. View All Tasks")
        print("3. View One Task")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                task_id = int(input("Task ID: "))
                title = input("Title: ")
                priority = input("Priority (low/medium/high): ")

                task = create_task({
                    "id": task_id,
                    "title": title,
                    "priority": priority
                })

                print("Created:", task)

            elif choice == "2":
                print(get_all_tasks())

            elif choice == "3":
                task_id = int(input("Task ID: "))
                print(get_task(task_id))

            elif choice == "4":
                task_id = int(input("Task ID: "))
                title = input("New Title: ")
                priority = input("New Priority: ")

                updated = update_task(
                    task_id,
                    {
                        "title": title,
                        "priority": priority
                    }
                )

                print("Updated:", updated)

            elif choice == "5":
                task_id = int(input("Task ID: "))
                delete_task(task_id)
                print("Task deleted")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid choice")

        except TaskNotFoundError as e:
            print("Error:", e)

        except ValidationError as e:
            print("Validation Error:")
            print(e)

        except ValueError as e:
            print("Error:", e)
menu()