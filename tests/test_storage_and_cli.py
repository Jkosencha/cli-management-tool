import json
import pytest
import main
from models import User, Project, Task
from utils import storage

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    db = tmp_path / "db.json"
    monkeypatch.setattr(storage, "DATA_FILE", str(db))
    User.reset()
    Project.reset()
    Task.reset()
    yield db

class TestStorage:
    def test_save_and_load_round_trip(self, isolated_db):
        alex = User("Alex", "alex@example.com")
        proj = Project("CLI Tool", due_date="2026-07-01")
        alex.add_project(proj)
        task = Task("Implement add-task")
        proj.add_task(task)
        task.assign_to(alex)

        storage.save_data()
        storage.load_data()

        user = User.find_by_name("Alex")
        project = Project.find_by_title("CLI Tool")
        loaded_task = Task.find_by_title("Implement add-task")
        assert user and project and loaded_task
        assert project.owner is user
        assert loaded_task.project is project
        assert user in loaded_task.contributors

    def test_load_missing_file_starts_empty(self, isolated_db):
        storage.load_data()
        assert User.all == [] and Project.all == [] and Task.all == []

    def test_load_corrupted_file_starts_fresh(self, isolated_db):
        isolated_db.write_text("{ this is not json !!")
        storage.load_data()  
        assert User.all == []

    def test_saved_file_is_valid_json(self, isolated_db):
        User("Alex")
        storage.save_data()
        payload = json.loads(isolated_db.read_text())
        assert payload["users"][0]["name"] == "Alex"
class TestCLI:
    def run(self, *argv):
        return main.main(list(argv))

    def test_add_and_list_user(self, capsys):
        assert self.run("add-user", "--name", "Alex", "--email", "alex@example.com") == 0
        assert "Added user" in capsys.readouterr().out
        assert self.run("list-users") == 0
        assert "Alex" in capsys.readouterr().out

    def test_duplicate_user_fails(self, capsys):
        self.run("add-user", "--name", "Alex")
        assert self.run("add-user", "--name", "Alex") == 1
        assert "already exists" in capsys.readouterr().out

    def test_add_project_requires_existing_user(self, capsys):
        assert self.run("add-project", "--user", "Ghost", "--title", "X") == 1
        assert "No user named" in capsys.readouterr().out

    def test_full_workflow(self, capsys):
        self.run("add-user", "--name", "Alex")
        self.run("add-project", "--user", "Alex", "--title", "CLI Tool",
                 "--due-date", "2026-07-01")
        self.run("add-task", "--project", "CLI Tool",
                 "--title", "Implement add-task", "--assign", "Alex")
        assert self.run("complete-task", "--title", "Implement add-task") == 0
        out = capsys.readouterr().out
        assert "complete" in out

        assert self.run("list-tasks", "--project", "CLI Tool") == 0
        assert "Implement add-task" in capsys.readouterr().out

    def test_search_projects(self, capsys):
        self.run("add-user", "--name", "Alex")
        self.run("add-project", "--user", "Alex", "--title", "CLI Tool")
        self.run("add-project", "--user", "Alex", "--title", "Website")
        capsys.readouterr()
        assert self.run("search-projects", "--keyword", "cli") == 0
        out = capsys.readouterr().out
        assert "CLI Tool" in out and "Website" not in out

    def test_update_task_invalid_status_rejected(self, capsys):
        self.run("add-user", "--name", "Alex")
        self.run("add-project", "--user", "Alex", "--title", "P")
        self.run("add-task", "--project", "P", "--title", "T")
        with pytest.raises(SystemExit): 
            self.run("update-task", "--title", "T", "--status", "nope")
