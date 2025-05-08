import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token
from app.models import load_users
from app.schemas import User

# TestClient instance for sending requests
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Setup mock users for testing (replicate user_data.json structure)
@pytest.fixture
def mock_users():
    return [
        User(id=1, username="admin", password="admin123", name="Alice", role="admin"),
        User(id=2, username="john", password="johnpass", name="John Doe", role="user"),
        User(id=3, username="jane", password="janepass", name="Jane Smith", role="user"),
        User(id=4, username="bob", password="bobpass", name="Bob", role="user"),
        User(id=5, username="eva", password="evapass", name="Eva", role="admin"),
        User(id=6, username="tom", password="tompass", name="Tom Hardy", role="user"),
        User(id=7, username="lisa", password="lisapass", name="Lisa Ray", role="manager"),
        User(id=8, username="raj", password="rajpass", name="Raj Kumar", role="user"),
        User(id=9, username="neha", password="nehapass", name="Neha Sharma", role="user"),
        User(id=10, username="mark", password="markpass", name="Mark Lee", role="manager")
    ]

# Fixture to create a JWT token for a user
@pytest.fixture
def token(mock_users):
    user = mock_users[0]  # Use the first user as a default (admin)
    return create_access_token(user)



@pytest.fixture(scope="session")
def session_scope_fixture():
    print("\n[Setup] Session-scope fixture")
    yield "session-scope"
    print("\n[Teardown] Session-scope fixture")

@pytest.fixture(scope="module")
def module_scope_fixture():
    print("\n[Setup] Module-scope fixture")
    yield "module-scope"
    print("\n[Teardown] Module-scope fixture")

@pytest.fixture(scope="function")
def function_scope_fixture():
    print("\n[Setup] Function-scope fixture")
    yield "function-scope"
    print("\n[Teardown] Function-scope fixture")

@pytest.fixture(scope="class")
def class_scope_fixture():
    print("\n[Setup] Class-scope fixture")
    yield "class-scope"
    print("\n[Teardown] Class-scope fixture")
