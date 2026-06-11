# Project Management CLI Tool

A Python command-line tool for managing users, projects, and tasks for a team of developers. Data is persisted locally as JSON, and output is rendered with tables via rich.

## Features

- Create and list **users** (Person > User inheritance, validated emails via @property setters)
- Add **projects** to users (one-to-many: User > Projects) with human-friendly due dates parsed by python **dateutil**
- Add **tasks** to projects (one-to-many: Project > Tasks) and assign multiple contributors (many-to-many: Tasks <> Users)
- Mark tasks complete, update their status/title, search projects by keyword
- Full JSON persistence with graceful handling of missing or corrupted data files
- Unit-tested with pytest (models, persistence, and CLI commands)

## Persistence

All data is stored in **data/db.json** and reloaded on every command. If the file is missing the tool starts with an empty database; if it's corrupted, a warning is logged and the tool starts fresh instead of crashing.
