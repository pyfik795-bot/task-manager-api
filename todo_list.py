import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title='task manager')


@app.get('/')
def home():
    return {'message':'my firs backend'}


class Task(BaseModel):
    title: str
    status: str = "todo"
    description: str = ""


tasks = [
    {"id": 1, "title": "Learn Python", "description": "", "status": "in_progress"},
    {"id": 2, "title": "Learn FastAPI", "description": "", "status": "todo"},
]

@app.get('/tasks')
def get_tasks():
    return tasks


@app.post('/tasks')
def create_task(task: Task):
    new_task = {
        'id' : len(tasks) + 1,
        'title': task.title,
        'status' : task.status,
        'description' : task.description
    }

    tasks.append(new_task)
    return new_task