import json
import os

from models import User, Project, Task

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "db.json")


def save_data(path=None):
    if path is None:
        path = DATA_FILE

    data = {
        "users": [user.to_dict() for user in User.all],
        "projects": [project.to_dict() for project in Project.all],
        "tasks": [task.to_dict() for task in Task.all],
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_data(path=None):
    if path is None:
        path = DATA_FILE

    User.reset()
    Project.reset()
    Task.reset()

    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    except json.JSONDecodeError:
        print(f"Warning: {path} is corrupted, starting with empty data.")
        return

    for user_info in data.get("users", []):
        User.from_dict(user_info)

    for project_info in data.get("projects", []):
        project = Project.from_dict(project_info)
        owner = User.find_by_name(project_info.get("owner") or "")
        if owner:
            owner.add_project(project)

    for task_info in data.get("tasks", []):
        task = Task.from_dict(task_info)
        project = Project.find_by_title(task_info.get("project") or "")
        if project:
            project.add_task(task)
        for name in task_info.get("assigned_to", []):
            user = User.find_by_name(name)
            if user:
                task.assign_to(user)