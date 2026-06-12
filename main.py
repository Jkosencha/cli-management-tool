import argparse
import sys

from models import User, Project, Task
from utils.storage import save_data, load_data
from utils import display


def cmd_add_user(args):
    if User.find_by_name(args.name):
        display.error(f"User '{args.name}' already exists.")
        return 1
    try:
        user = User(name=args.name, email=args.email or "")
    except ValueError as exc:
        display.error(str(exc))
        return 1
    save_data()
    display.success(f"Added user: {user}")
    return 0


def cmd_list_users(args):
    if not User.all:
        display.info("No users yet. Add one with: add-user --name \"Alex\"")
        return 0
    display.users_table(User.all)
    return 0


def cmd_add_project(args):
    user = User.find_by_name(args.user)
    if user is None:
        display.error(f"No user named '{args.user}'. Create them first with add-user.")
        return 1
    if Project.find_by_title(args.title):
        display.error(f"A project titled '{args.title}' already exists.")
        return 1
    try:
        project = Project(title=args.title, description=args.description or "",
                          due_date=args.due_date or "")
    except ValueError as exc:
        display.error(str(exc))
        return 1
    user.add_project(project)
    save_data()
    display.success(f"Added project '{project.title}' for {user.name}.")
    return 0


def cmd_list_projects(args):
    if args.user:
        user = User.find_by_name(args.user)
        if user is None:
            display.error(f"No user named '{args.user}'.")
            return 1
        if not user.projects:
            display.info(f"{user.name} has no projects yet.")
            return 0
        display.projects_table(user.projects, title=f"Projects for {user.name}")
    else:
        if not Project.all:
            display.info("No projects yet.")
            return 0
        display.projects_table(Project.all)
    return 0


def cmd_search_projects(args):
    keyword = args.keyword.lower()
    matches = [p for p in Project.all
               if keyword in p.title.lower() or keyword in p.description.lower()]
    if not matches:
        display.info(f"No projects matching '{args.keyword}'.")
        return 0
    display.projects_table(matches, title=f"Projects matching '{args.keyword}'")
    return 0


def cmd_add_task(args):
    project = Project.find_by_title(args.project)
    if project is None:
        display.error(f"No project titled '{args.project}'.")
        return 1
    try:
        task = Task(title=args.title, status=args.status)
    except ValueError as exc:
        display.error(str(exc))
        return 1
    project.add_task(task)
    if args.assign:
        for name in args.assign:
            user = User.find_by_name(name)
            if user is None:
                display.error(f"No user named '{name}' — skipping assignment.")
                continue
            task.assign_to(user)
    save_data()
    display.success(f"Added task '{task.title}' to project '{project.title}'.")
    return 0


def cmd_list_tasks(args):
    if args.project:
        project = Project.find_by_title(args.project)
        if project is None:
            display.error(f"No project titled '{args.project}'.")
            return 1
        if not project.tasks:
            display.info(f"'{project.title}' has no tasks yet.")
            return 0
        display.tasks_table(project.tasks, title=f"Tasks in '{project.title}'")
    else:
        if not Task.all:
            display.info("No tasks yet.")
            return 0
        display.tasks_table(Task.all)
    return 0


def cmd_complete_task(args):
    task = Task.find_by_title(args.title)
    if task is None:
        display.error(f"No task titled '{args.title}'.")
        return 1
    task.complete()
    save_data()
    if task.project:
        display.success(f"Marked '{task.title}' as complete. ({task.project.progress})")
    else:
        display.success(f"Marked '{task.title}' as complete.")
    return 0


def cmd_update_task(args):
    task = Task.find_by_title(args.title)
    if task is None:
        display.error(f"No task titled '{args.title}'.")
        return 1
    try:
        if args.status:
            task.status = args.status
        if args.new_title:
            task.title = args.new_title
    except ValueError as exc:
        display.error(str(exc))
        return 1
    save_data()
    display.success(f"Updated task: {task}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pm",
        description="A command-line project management tool for teams.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-user", help="Create a new user.")
    p.add_argument("--name", required=True, help="Full name of the user.")
    p.add_argument("--email", help="Email address (optional).")
    p.set_defaults(func=cmd_add_user)

    p = sub.add_parser("list-users", help="List all users.")
    p.set_defaults(func=cmd_list_users)

    p = sub.add_parser("add-project", help="Create a project for a user.")
    p.add_argument("--user", required=True, help="Owner's name.")
    p.add_argument("--title", required=True, help="Project title.")
    p.add_argument("--description", help="Short description.")
    p.add_argument("--due-date", help="Due date (e.g. 2026-07-01 or 'July 1 2026').")
    p.set_defaults(func=cmd_add_project)

    p = sub.add_parser("list-projects", help="List projects (optionally for one user).")
    p.add_argument("--user", help="Only show projects owned by this user.")
    p.set_defaults(func=cmd_list_projects)

    p = sub.add_parser("search-projects", help="Search projects by keyword.")
    p.add_argument("--keyword", required=True, help="Keyword to match in title/description.")
    p.set_defaults(func=cmd_search_projects)

    p = sub.add_parser("add-task", help="Add a task to a project.")
    p.add_argument("--project", required=True, help="Project title.")
    p.add_argument("--title", required=True, help="Task title.")
    p.add_argument("--status", default="pending",
                   choices=Task.VALID_STATUSES, help="Initial status.")
    p.add_argument("--assign", nargs="*",
                   help="One or more user names to assign as contributors.")
    p.set_defaults(func=cmd_add_task)

    p = sub.add_parser("list-tasks", help="List tasks (optionally for one project).")
    p.add_argument("--project", help="Only show tasks in this project.")
    p.set_defaults(func=cmd_list_tasks)

    p = sub.add_parser("complete-task", help="Mark a task as complete.")
    p.add_argument("--title", required=True, help="Task title.")
    p.set_defaults(func=cmd_complete_task)

    p = sub.add_parser("update-task", help="Update a task's status or title.")
    p.add_argument("--title", required=True, help="Current task title.")
    p.add_argument("--status", choices=Task.VALID_STATUSES, help="New status.")
    p.add_argument("--new-title", help="New title.")
    p.set_defaults(func=cmd_update_task)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    load_data()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())