from dateutil import parser as date_parser
class Project:
    _id_counter = 1
    all = []

    def __init__(self, title, description="", due_date="", project_id=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = None   
        self.tasks = []

        if project_id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = project_id
            Project._id_counter = max(Project._id_counter, project_id + 1)

        Project.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project title must be a non-empty string.")
        self._title = value.strip()

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        value = (value or "").strip()
        if value:
            try:
                value = date_parser.parse(value).date().isoformat()
            except (ValueError, OverflowError):
                raise ValueError(f"Could not understand due date '{value}'.")
        self._due_date = value

    def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)
            task.project = self

    @property
    def progress(self):
        if not self.tasks:
            return "no tasks"
        done = sum(1 for t in self.tasks if t.status == "complete")
        return f"{done}/{len(self.tasks)} tasks complete"

    @classmethod
    def find_by_title(cls, title):
        title = title.strip().lower()
        for project in cls.all:
            if project.title.lower() == title:
                return project
        return None

    @classmethod
    def reset(cls):
        cls.all = []
        cls._id_counter = 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner.name if self.owner else None,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            project_id=data.get("id"),
        )

    def __str__(self):
        due = f" (due {self.due_date})" if self.due_date else ""
        return f"[{self.id}] {self.title}{due} - {self.progress}"

    def __repr__(self):
        return f"Project(title={self.title!r}, due_date={self.due_date!r})"