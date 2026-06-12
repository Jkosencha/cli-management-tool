import pytest

from models import User, Project, Task

@pytest.fixture(autouse=True)
def clean_registries():
    User.reset()
    Project.reset()
    Task.reset()
    yield

class TestUser:
    def test_create_user(self):
        u = User("Alex", "alex@example.com")
        assert u.name == "Alex"
        assert u.email == "alex@example.com"
        assert u in User.all

    def test_id_counter_increments(self):
        a = User("A")
        b = User("B")
        assert b.id == a.id + 1

    def test_invalid_name_raises(self):
        with pytest.raises(ValueError):
            User("   ")

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            User("Alex", "not-an-email")

    def test_find_by_name_case_insensitive(self):
        User("Alex")
        assert User.find_by_name("alex") is not None
        assert User.find_by_name("Nobody") is None

    def test_round_trip_serialization(self):
        u = User("Alex", "alex@example.com")
        data = u.to_dict()
        User.reset()
        restored = User.from_dict(data)
        assert restored.name == "Alex"
        assert restored.id == u.id

class TestProject:
    def test_user_project_relationship(self):
        u = User("Alex")
        p = Project("CLI Tool")
        u.add_project(p)
        assert p in u.projects
        assert p.owner is u

    def test_due_date_normalization(self):
        p = Project("X", due_date="July 1 2026")
        assert p.due_date == "2026-07-01"

    def test_bad_due_date_raises(self):
        with pytest.raises(ValueError):
            Project("X", due_date="not a date")

    def test_empty_title_raises(self):
        with pytest.raises(ValueError):
            Project("")

    def test_progress_property(self):
        p = Project("X")
        assert p.progress == "no tasks"
        t1, t2 = Task("a"), Task("b")
        p.add_task(t1)
        p.add_task(t2)
        t1.complete()
        assert p.progress == "1/2 tasks complete"

class TestTask:
    def test_default_status(self):
        assert Task("Write tests").status == "pending"

    def test_complete(self):
        t = Task("Write tests")
        t.complete()
        assert t.status == "complete"

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError):
            Task("X", status="done-ish")

    def test_many_to_many_contributors(self):
        t = Task("Pair task")
        a, b = User("A"), User("B")
        t.assign_to(a)
        t.assign_to(b)
        t.assign_to(a)  
        assert t.contributors == [a, b]

    def test_project_task_relationship(self):
        p = Project("CLI Tool")
        t = Task("Implement add-task")
        p.add_task(t)
        assert t.project is p
        assert t in p.tasks
