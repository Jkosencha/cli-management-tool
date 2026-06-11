# Project Management CLI Tool

A Python command-line tool for managing users, projects, and tasks for a team of developers. Data is persisted locally as JSON, and output is rendered with pretty tables via [rich](https://github.com/Textualize/rich).

## Features

- Create and list **users** (`Person → User` inheritance, validated emails via `@property` setters)
- Add **projects** to users (one-to-many: User → Projects) with human-friendly due dates parsed by `python-dateutil` (`--due-date "July 1 2026"` works)
- Add **tasks** to projects (one-to-many: Project → Tasks) and assign multiple contributors (many-to-many: Tasks ↔ Users)
- Mark tasks complete, update their status/title, search projects by keyword
- Full JSON persistence with graceful handling of missing or corrupted data files
- Unit-tested with `pytest` (models, persistence, and CLI commands)

## Project structure

```
project-manager-cli/
├── main.py              # CLI entry point (argparse subcommands)
├── models/              # Class definitions
│   ├── person.py        # Base Person class (inheritance)
│   ├── user.py          # User (one-to-many → Projects)
│   ├── project.py       # Project (one-to-many → Tasks)
│   └── task.py          # Task (many-to-many contributors)
├── utils/
│   ├── storage.py       # JSON save/load with error handling
│   └── display.py       # rich-based table output helpers
├── data/
│   └── db.json          # Local JSON datastore (created automatically)
├── tests/
│   ├── test_models.py
│   └── test_storage_and_cli.py
├── requirements.txt
└── README.md
```

## Setup

Requires Python 3.10+.

```bash
git clone <your-repo-url>
cd project-manager-cli
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Get help for any command with `-h`:

```bash
python main.py -h
python main.py add-project -h
```

### Manage users

```bash
python main.py add-user --name "Alex" --email alex@example.com
python main.py list-users
```

### Manage projects

```bash
python main.py add-project --user "Alex" --title "CLI Tool" \
    --description "Build a project tracker" --due-date 2026-07-01

python main.py list-projects                 # all projects
python main.py list-projects --user "Alex"   # one user's projects
python main.py search-projects --keyword cli
```

### Manage tasks

```bash
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assign "Alex"
python main.py list-tasks --project "CLI Tool"
python main.py complete-task --title "Implement add-task"
python main.py update-task --title "Implement add-task" --status in-progress
```

Valid task statuses: `pending`, `in-progress`, `complete`.

## Persistence

All data is stored in `data/db.json` and reloaded on every command. If the file is missing the tool starts with an empty database; if it's corrupted, a warning is logged and the tool starts fresh instead of crashing.

## Running the tests

```bash
pytest -v
```

Tests cover model validation, object relationships, ID counters, JSON round-trips, corrupted-file handling, and end-to-end CLI workflows (using pytest's `tmp_path` and `monkeypatch` so they never touch your real data file).

## Debugging

Pass `-v` / `--verbose` before a subcommand to enable debug logging:

```bash
python main.py -v list-projects
```

## Dependencies

| Package | Purpose |
|---|---|
| `rich` | Colored, tabular CLI output |
| `python-dateutil` | Flexible due-date parsing |
| `pytest` | Test runner |
