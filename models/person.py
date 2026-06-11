class Person:

    def __init__(self, name: str, email: str = ""):
        self.name = name     
        self.email = email    

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        value = (value or "").strip()
        if value and ("@" not in value or "." not in value.split("@")[-1]):
            raise ValueError(f"'{value}' is not a valid email address.")
        self._email = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, email={self.email!r})"
