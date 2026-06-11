from rich.console import Console
from rich.table import Table

console = Console()


def success(msg: str) -> None:
    console.print(f"[bold green]✔[/] {msg}")


def error(msg: str) -> None:
    console.print(f"[bold red]✘[/] {msg}")


def info(msg: str) -> None:
    console.print(f"[bold cyan]ℹ[/] {msg}")


def users_table(users) -> None:
    table = Table(title="Users")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Email")
    table.add_column("Projects", justify="right")
    for u in users:
        table.add_row(str(u.id), u.name, u.email or "—", str(len(u.projects)))
    console.print(table)


def projects_table(projects, title: str = "Projects") -> None:
    table = Table(title=title)
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Owner")
    table.add_column("Due date")
    table.add_column("Progress")
    for p in projects:
        owner = p.owner.name if p.owner else "—"
        table.add_row(str(p.id), p.title, owner, p.due_date or "—", p.progress)
    console.print(table)


def tasks_table(tasks, title: str = "Tasks") -> None:
    table = Table(title=title)
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Status")
    table.add_column("Project")
    table.add_column("Assigned to")
    for t in tasks:
        status_style = {"complete": "green", "in-progress": "yellow",
                        "pending": "red"}.get(t.status, "white")
        project = t.project.title if t.project else "—"
        people = ", ".join(u.name for u in t.contributors) or "—"
        table.add_row(str(t.id), t.title, f"[{status_style}]{t.status}[/]", project, people)
    console.print(table)
