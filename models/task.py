class Task:
    _id_counter: int = 1
    all: list["Task"] = []

    VALID_STATUSES = ("pending", "in-progress", "complete")

    def __init__(self, title: str, status: str = "pending",
                 task_id: int | None = None):
        self.title = title
        self.status = status
        self.project = None       
        self.contributors: list = [] 
        if task_id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = task_id
            Task._id_counter = max(Task._id_counter, task_id + 1)
        Task.all.append(self)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title must be a non-empty string.")
        self._title = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        value = (value or "").strip().lower()
        if value not in self.VALID_STATUSES:
            raise ValueError(
                f"Status must be one of {', '.join(self.VALID_STATUSES)}; got '{value}'."
            )
        self._status = value

    def complete(self) -> None:
        self.status = "complete"

    def assign_to(self, user) -> None:
        """Add a contributor (many-to-many)."""
        if user not in self.contributors:
            self.contributors.append(user)

    @classmethod
    def find_by_title(cls, title: str) -> "Task | None":
        title = title.strip().lower()
        return next((t for t in cls.all if t.title.lower() == title), None)

    @classmethod
    def reset(cls) -> None:
        cls.all = []
        cls._id_counter = 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "project": self.project.title if self.project else None,
            "assigned_to": [u.name for u in self.contributors],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data["title"],
            status=data.get("status", "pending"),
            task_id=data.get("id"),
        )

    def __str__(self) -> str:
        people = ", ".join(u.name for u in self.contributors) or "unassigned"
        return f"[{self.id}] {self.title} ({self.status}) — {people}"

    def __repr__(self) -> str:
        return f"Task(title={self.title!r}, status={self.status!r})"
