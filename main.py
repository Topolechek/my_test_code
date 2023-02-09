from fastapi import FastAPI
from typing import Tuple
from enum import Enum
import asyncio
import uuid

app = FastAPI()

class TaskStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"

tasks = {}

async def background_task(task_id, x, y, operator):
    result = None
    status = TaskStatus.SUCCESS
    try:
        if operator == "+":
            result = x + y
        elif operator == "-":
            result = x - y
        elif operator == "*":
            result = x * y
        elif operator == "/":
            result = x / y
        else:
            status = TaskStatus.FAILURE
    except Exception as e:
        status = TaskStatus.FAILURE
    tasks[task_id] = {"status": status, "result": result}

@app.post("/task")
async def create_task(x: int, y: int, operator: str):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": TaskStatus.PENDING, "result": None}
    asyncio.create_task(background_task(task_id, x, y, operator))
    return {"task_id": task_id}

@app.get("/task/{task_id}")
async def get_task_result(task_id: str):
    if task_id in tasks:
        task = tasks[task_id]
        if task["status"] == TaskStatus.SUCCESS:
            return {"status": task["status"], "result": task["result"]}
        else:
            return {"status": task["status"], "result": None}
    else:
        return {"status": TaskStatus.FAILURE, "result": None}

@app.get("/tasks")
async def get_tasks_status():
    return {"tasks": tasks}