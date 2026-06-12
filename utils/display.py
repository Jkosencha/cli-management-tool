from rich.console import Console
from rich.table import Table

console = Console()

def success(msg):
    console.print(f"[bold green]Success:[/] {msg}")


def error(msg):
    console.print(f"[bold red]Error:[/] {msg}")


def info(msg):
    console.print(f"[bold cyan]Info:[/] {msg}")


def users_table(users):
    table = Table(title="Users")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Email")
    table.add_column("Projects", justify="right")

    for user in users:
        table.add_row(str(user.id), user.name, user.email or "-",
                      str(len(user.projects)))
    console.print(table)


def projects_table(projects, title="Projects"):
    table = Table(title=title)
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Owner")
    table.add_column("Due date")
    table.add_column("Progress")

    for project in projects:
        owner = project.owner.name if project.owner else "-"
        table.add_row(str(project.id), project.title, owner,
                      project.due_date or "-", project.progress)
    console.print(table)


def tasks_table(tasks, title="Tasks"):
    colors = {"complete": "green", "in-progress": "yellow", "pending": "red"}

    table = Table(title=title)
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Status")
    table.add_column("Project")
    table.add_column("Assigned to")

    for task in tasks:
        color = colors.get(task.status, "white")
        project = task.project.title if task.project else "-"
        people = ", ".join(u.name for u in task.contributors) or "-"
        table.add_row(str(task.id), task.title,
                      f"[{color}]{task.status}[/]", project, people)
    console.print(table)