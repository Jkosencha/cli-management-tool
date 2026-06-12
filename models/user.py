from models.person import Person
class User(Person):
    _id_counter = 1
    all = []

    def __init__(self, name, email="", user_id=None):
        super().__init__(name, email)

        if user_id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = user_id
            User._id_counter = max(User._id_counter, user_id + 1)

        self.projects = []
        User.all.append(self)

    def add_project(self, project):
        if project not in self.projects:
            self.projects.append(project)
            project.owner = self

    @classmethod
    def find_by_name(cls, name):
        name = name.strip().lower()
        for user in cls.all:
            if user.name.lower() == name:
                return user
        return None

    @classmethod
    def reset(cls):
        cls.all = []
        cls._id_counter = 1

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], email=data.get("email", ""),
                   user_id=data.get("id"))

    def __str__(self):
        email = f" <{self.email}>" if self.email else ""
        return f"[{self.id}] {self.name}{email} - {len(self.projects)} project(s)"