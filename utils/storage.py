import json
import logging
import os

from models import User, Project, Task

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DATA_FILE = os.path.join(DATA_DIR, "db.json")

def save_data(path: str | None = None) -> None:
    path = path or DATA_FILE  
    payload = {
        "users": [u.to_dict() for u in User.all],
        "projects": [p.to_dict() for p in Project.all],
        "tasks": [t.to_dict() for t in Task.all],
    }
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.debug("Saved %d users, %d projects, %d tasks to %s",
                     len(User.all), len(Project.all), len(Task.all), path)
    except OSError as exc:
        logger.error("Could not write data file %s: %s", path, exc)
        raise

def load_data(path: str | None = None) -> None:
    path = path or DATA_FILE  
    User.reset()
    Project.reset()
    Task.reset()

    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
    except FileNotFoundError:
        logger.debug("No data file at %s — starting with an empty database.", path)
        return
    except json.JSONDecodeError as exc:
        logger.warning("Data file %s is corrupted (%s). Starting fresh.", path, exc)
        return

    for u in payload.get("users", []):
        try:
            User.from_dict(u)
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping bad user record %r: %s", u, exc)

    for p in payload.get("projects", []):
        try:
            project = Project.from_dict(p)
            owner = User.find_by_name(p.get("owner") or "")
            if owner:
                owner.add_project(project)
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping bad project record %r: %s", p, exc)

    for t in payload.get("tasks", []):
        try:
            task = Task.from_dict(t)
            project = Project.find_by_title(t.get("project") or "")
            if project:
                project.add_task(task)
            for name in t.get("assigned_to", []):
                user = User.find_by_name(name)
                if user:
                    task.assign_to(user)
        except (KeyError, ValueError) as exc:
            logger.warning("Skipping bad task record %r: %s", t, exc)
