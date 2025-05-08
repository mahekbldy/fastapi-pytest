from unittest.mock import Mock, patch, MagicMock

import pytest
from fastapi import HTTPException, status
from app.main import app
from app.auth import authenticate_user, create_access_token
from app.schemas import Token, User


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


def test_login_success_with_mock(client):
    """Test login by mocking authenticate_user with Mock."""
    mock_auth = Mock()

    mock_auth.return_value = User(id=99, username="mockeduser", password="admin123", name="Mocked Name", role="tester")

    with patch("app.routes.auth.authenticate_user", mock_auth):
        response = client.post("/auth/login", data={"username": "mockeduser", "password": "secret"})
        assert response.status_code == 200
        json_data = response.json()
        assert "access_token" in json_data
        assert mock_auth.call_count == 1


def test_login_success_with_magicmock(client):
    """Test login by mocking authenticate_user with MagicMock."""
    mock_auth = MagicMock()

    mock_auth.return_value = User(
        id=99,
        username="mockeduser",
        password="admin123",
        name="Mocked Name",
        role="tester"
    )

    with patch("app.routes.auth.authenticate_user", mock_auth):
        response = client.post("/auth/login", data={"username": "mockeduser", "password": "secret"})
        assert response.status_code == 200
        json_data = response.json()
        assert "access_token" in json_data
        assert mock_auth.call_count == 1