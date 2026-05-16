import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for tests
TEST_DB_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_client(client):
    """Register + login, return authenticated client with token header."""
    client.post("/users/", json={
        "username": "testuser", "email": "test@test.com", "password": "pass123"
    })
    resp = client.post("/token", data={"username": "testuser", "password": "pass123"})
    token = resp.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


# ── User & Auth Tests ─────────────────────────────────────────
class TestAuth:
    def test_register_user(self, client):
        r = client.post("/users/", json={
            "username": "alice", "email": "alice@test.com", "password": "secret"
        })
        assert r.status_code == 201
        assert r.json()["username"] == "alice"

    def test_register_duplicate_username(self, client):
        client.post("/users/", json={"username": "bob", "email": "bob@test.com", "password": "x"})
        r = client.post("/users/", json={"username": "bob", "email": "bob2@test.com", "password": "x"})
        assert r.status_code == 400

    def test_login_success(self, client):
        client.post("/users/", json={"username": "carol", "email": "c@t.com", "password": "pw"})
        r = client.post("/token", data={"username": "carol", "password": "pw"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_wrong_password(self, client):
        client.post("/users/", json={"username": "dave", "email": "d@t.com", "password": "right"})
        r = client.post("/token", data={"username": "dave", "password": "wrong"})
        assert r.status_code == 401


# ── Todo CRUD Tests ───────────────────────────────────────────
class TestTodos:
    def test_create_todo(self, auth_client):
        r = auth_client.post("/todos/", json={"title": "Buy milk", "category": "shopping"})
        assert r.status_code == 201
        assert r.json()["title"] == "Buy milk"

    def test_list_todos(self, auth_client):
        auth_client.post("/todos/", json={"title": "Task 1"})
        auth_client.post("/todos/", json={"title": "Task 2"})
        r = auth_client.get("/todos/")
        assert r.status_code == 200
        assert r.json()["total"] == 2

    def test_get_todo_by_id(self, auth_client):
        created = auth_client.post("/todos/", json={"title": "My task"}).json()
        r = auth_client.get(f"/todos/{created['id']}")
        assert r.status_code == 200
        assert r.json()["title"] == "My task"

    def test_get_nonexistent_todo(self, auth_client):
        r = auth_client.get("/todos/9999")
        assert r.status_code == 404

    def test_update_todo(self, auth_client):
        todo = auth_client.post("/todos/", json={"title": "Old title"}).json()
        r = auth_client.put(f"/todos/{todo['id']}", json={"title": "New title", "completed": True})
        assert r.status_code == 200
        assert r.json()["title"] == "New title"
        assert r.json()["completed"] is True

    def test_patch_todo(self, auth_client):
        todo = auth_client.post("/todos/", json={"title": "Patch me"}).json()
        r = auth_client.patch(f"/todos/{todo['id']}", json={"completed": True})
        assert r.status_code == 200
        assert r.json()["completed"] is True

    def test_delete_todo(self, auth_client):
        todo = auth_client.post("/todos/", json={"title": "Delete me"}).json()
        r = auth_client.delete(f"/todos/{todo['id']}")
        assert r.status_code == 204
        assert auth_client.get(f"/todos/{todo['id']}").status_code == 404

    def test_filter_by_completed(self, auth_client):
        auth_client.post("/todos/", json={"title": "Done"})
        todo = auth_client.post("/todos/", json={"title": "Pending"}).json()
        auth_client.put(f"/todos/{todo['id']}", json={"completed": True})
        r = auth_client.get("/todos/?completed=false")
        assert all(not t["completed"] for t in r.json()["items"])

    def test_filter_by_category(self, auth_client):
        auth_client.post("/todos/", json={"title": "Work task", "category": "work"})
        auth_client.post("/todos/", json={"title": "Home task", "category": "home"})
        r = auth_client.get("/todos/?category=work")
        assert r.json()["total"] == 1
        assert r.json()["items"][0]["category"] == "work"

    def test_pagination(self, auth_client):
        for i in range(15):
            auth_client.post("/todos/", json={"title": f"Task {i}"})
        r = auth_client.get("/todos/?page=1&page_size=5")
        assert len(r.json()["items"]) == 5
        assert r.json()["total"] == 15

    def test_unauthorized_access(self, client):
        r = client.get("/todos/")
        assert r.status_code == 401

    def test_cannot_access_other_users_todo(self, client):
        # User 1
        client.post("/users/", json={"username": "u1", "email": "u1@t.com", "password": "pw"})
        t1 = client.post("/token", data={"username": "u1", "password": "pw"}).json()["access_token"]
        headers1 = {"Authorization": f"Bearer {t1}"}
        todo = client.post("/todos/", json={"title": "Private"}, headers=headers1).json()

        # User 2 tries to access User 1's todo
        client.post("/users/", json={"username": "u2", "email": "u2@t.com", "password": "pw"})
        t2 = client.post("/token", data={"username": "u2", "password": "pw"}).json()["access_token"]
        headers2 = {"Authorization": f"Bearer {t2}"}
        r = client.get(f"/todos/{todo['id']}", headers=headers2)
        assert r.status_code == 404
