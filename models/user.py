from models.person import Person
class User(Person):
    _id_counter: int = 1
    all: list["User"] = []

    def __init__(self, name: str, email: str = "", user_id: int | None = None):
        super().__init__(name, email)
        if user_id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = user_id
            User._id_counter = max(User._id_counter, user_id + 1)
        self.projects: list = [] 
        User.all.append(self)

    def add_project(self, project) -> None:
        if project not in self.projects:
            self.projects.append(project)
            project.owner = self

    @classmethod
    def find_by_name(cls, name: str) -> "User | None":
        name = name.strip().lower()
        return next((u for u in cls.all if u.name.lower() == name), None)

    @classmethod
    def reset(cls) -> None:
        cls.all = []
        cls._id_counter = 1

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(name=data["name"], email=data.get("email", ""), user_id=data.get("id"))

    def __str__(self) -> str:
        email = f" <{self.email}>" if self.email else ""
        return f"[{self.id}] {self.name}{email} — {len(self.projects)} project(s)"
