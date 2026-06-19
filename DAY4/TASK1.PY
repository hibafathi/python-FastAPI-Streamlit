from pydantic import BaseModel,ValidationError
class TaskModel(BaseModel):
    title:str
    priority:str="low"
    completed:bool=False
task=TaskModel(title="study python")
print(task)
print("\n testing validation error\n")
try:
    task2=TaskModel(title=123,completed="abs"
                    )
except ValidationError as e:
    print(e)