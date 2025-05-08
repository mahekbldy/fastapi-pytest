import pytest
from fastapi import HTTPException, status
from app.main import app
from app.auth import authenticate_user, create_access_token
from app.schemas import Token

# Test Login Endpoint
def test_login_success(client, mock_users):
    """Test successful login with valid credentials."""
    valid_user = mock_users[0]  # First user (Alice)
    response = client.post(
        "/auth/login", data={"username": valid_user.username, "password": valid_user.password}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_failure(client, mock_users):
    """Test failed login with invalid credentials."""
    invalid_username = "nonexistentuser"
    response = client.post(
        "/auth/login", data={"username": invalid_username, "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
