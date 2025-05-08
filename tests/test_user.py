from fastapi.testclient import TestClient
from app.main import app  # FastAPI app import
from unittest.mock import patch

# Test User Listing with Filters
def test_list_users_with_filters(client, token):
    """Test the /users endpoint with various filters."""

    headers = {"Authorization": f"Bearer {token}"}

    # Test filter by id
    response = client.get("/users/?id=1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1

    # Test filter by name (case-insensitive)
    response = client.get("/users/?name=alice", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"].lower() == "alice"

    # Test filter by role
    response = client.get("/users/?role=user", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 6  # 7 users have "user" role

    # Test multiple filters (id and role)
    response = client.get("/users/?id=3&role=user", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 3
    assert response.json()[0]["role"] == "user"

    # Test invalid filter (non-existing user id)
    response = client.get("/users/?id=999", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0  # No users with id 999


def test_user_unauthorized(client):
    """Test unauthorized access to /users endpoint."""
    response = client.get("/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_filter_by_id(client, token):
    """Test filtering users by ID."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?id=1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1


def test_filter_by_name(client, token):
    """Test filtering users by name (case-insensitive)."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?name=alice", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"].lower() == "alice"


def test_filter_by_role(client, token):
    """Test filtering users by role."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?role=user", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 6  # 6 users have the "user" role


def test_filter_by_multiple_params(client, token):
    """Test filtering users by multiple parameters."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?id=3&role=user", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 3
    assert response.json()[0]["role"] == "user"


def test_filter_with_invalid_id(client, token):
    """Test filtering users with a non-existing user ID."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?id=999", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0  # No users with ID 999




mock_user_data = [
    {"id": 10, "username": "mocker", "password": "secret", "name": "Mock M", "role": "tester"},
    {"id": 11, "username": "fake", "password": "fake", "name": "Fake User", "role": "user"},
]


@patch("app.routes.users.load_users", return_value=mock_user_data)
def test_users_with_mocked_data(mock_load, client, token):
    """Test /users with a mocked load_users function."""
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Mock M"
    assert mock_load.called


@patch("app.routes.users.load_users", return_value=[])
def test_users_empty_list(mock_load, client, token):
    """Test /users returns empty list if load_users returns nothing."""
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users", headers=headers)

    assert response.status_code == 200
    assert response.json() == []
