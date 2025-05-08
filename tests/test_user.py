from fastapi.testclient import TestClient
from app.main import app  # FastAPI app import

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
