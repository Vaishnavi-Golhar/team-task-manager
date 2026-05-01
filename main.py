from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Team Task Manager API",
    version="1.0.0"
)

# Dummy DB
users = []
projects = []
tasks = []

# Models
class User(BaseModel):
    name: str
    email: str
    password: str
    role: str

class Project(BaseModel):
    name: str
    created_by: str

class Task(BaseModel):
    title: str
    project: str
    assigned_to: str
    status: str = "todo"

# Auth
@app.post("/signup")
def signup(user: User):
    users.append(user)
    return {"message": "User created"}

@app.post("/login")
def login(email: str, password: str):
    for u in users:
        if u.email == email and u.password == password:
            return {"message": "Login success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Projects
@app.post("/projects")
def create_project(project: Project):
    projects.append(project)
    return {"message": "Project created"}

@app.get("/projects")
def get_projects():
    return projects

# Tasks
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, status: str):
    if task_id < len(tasks):
        tasks[task_id].status = status
        return {"message": "Updated"}
    raise HTTPException(status_code=404, detail="Task not found")

# Dashboard
@app.get("/dashboard")
def dashboard():
    total = len(tasks)
    done = len([t for t in tasks if t.status == "done"])
    return {
        "total_tasks": total,
        "completed_tasks": done
    }