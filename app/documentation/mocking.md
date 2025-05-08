# 🎭 Mocking in Pytest using `unittest.mock` – Complete Guide

---

## 🔍 What is Mocking?

**Mocking** is the process of replacing real objects or functions with **fake (mocked) versions** to isolate behavior during testing.

- Use when you don’t want to call actual dependencies (e.g., database, API, function).
- Common for testing in isolation, verifying calls, and controlling return values.

---

## 📦 Tools Used

- Python’s built-in `unittest.mock`
- Key functions: `@patch`, `Mock`, `MagicMock`, `patch.object`, `patch.dict`

---


# ✅ Using @patch to Simulate /users API in Pytest

This section demonstrates how to use the `patch` decorator from Python's `unittest.mock` library to simulate the `/users` API in FastAPI. The test mocks the `load_users` function, which would normally fetch users from a database or another source, and returns mock data instead.

---

## 🧪 Test Case: `test_users_with_mocked_data`

```python
# test_user.py

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
```
- 🔍 Explanation

| Line                                                                 | Description                                                                                                                                                                                                                 |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mock_user_data = [...]`                                             | This list contains the mock user data that will be returned by the `load_users` function. This is what the `/users` endpoint will use for the test.                                                                         |
| `@patch("app.routes.users.load_users", return_value=mock_user_data)` | The `patch` decorator is used to replace the `load_users` function in the `app.routes.users` module with a mock version that returns the `mock_user_data`. This prevents actual database or external calls during the test. |
| `def test_users_with_mocked_data(mock_load, client, token):`         | This test case will use the mocked `load_users` function and test the `/users` endpoint. The `mock_load` argument represents the mocked function, while `client` and `token` are provided by pytest fixtures.               |
| `headers = {"Authorization": f"Bearer {token}"}`                     | The `Authorization` header is set with the `Bearer` token, which is required for authentication to access the `/users` endpoint.                                                                                            |
| `response = client.get("/users", headers=headers)`                   | This simulates an HTTP GET request to the `/users` endpoint with the given authorization token.                                                                                                                             |
| `assert response.status_code == 200`                                 | Asserts that the response status code is 200, meaning the request was successful.                                                                                                                                           |
| `assert len(data) == 2`                                              | Verifies that the response data contains 2 users, which matches the length of `mock_user_data`.                                                                                                                             |
| `assert data[0]["name"] == "Mock M"`                                 | Checks that the name of the first user in the response matches the expected value "Mock M".                                                                                                                                 |
| `assert mock_load.called`                                            | Verifies that the `load_users` function (mocked by `patch`) was called during the test.                                                                                                                                     |



# ✅ Using Mock to Simulate Login Behavior in Pytest

This section demonstrates how to use Python's `unittest.mock.Mock` to simulate the behavior of `authenticate_user` in our FastAPI project for testing login functionality without executing actual authentication logic.

---

## 🧪 Test Case: `test_login_success_with_mock`


```python
#test_auth.py
def test_login_success_with_mock(client):
    """Test login by mocking authenticate_user with Mock."""
    mock_auth = Mock()
    
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
```
- 🔍 Explanation

| Line                                                    | Description                                                                                                                                                                                       |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mock_auth = Mock()`                                    | Creates a mock object that will simulate the behavior of the `authenticate_user` function during the test.                                                                                        |
| `mock_auth.return_value = User(...)`                    | This tells the mock object to return a predefined `User` object whenever it is called. We are simulating the scenario where a user with the given credentials exists and can successfully log in. |
| `patch("app.routes.auth.authenticate_user", mock_auth)` | This line uses `patch` to temporarily replace the real `authenticate_user` function in the `auth` module with our mock object during the execution of the test.                                   |
| `client.post(...)`                                      | This simulates a POST request to the login endpoint of your FastAPI app, with the username and password as inputs.                                                                                |
| `assert response.status_code == 200`                    | Since the `authenticate_user` function is mocked to return a valid user, we assert that the response status is 200, meaning the login was successful.                                             |
| `assert "access_token" in response.json()`              | After a successful login, the response should include an "access\_token" (JWT). This assertion ensures that the token is returned in the response.                                                |
| `assert mock_auth.call_count == 1`                      | This checks how many times the `mock_auth` function was called. We expect it to have been called exactly once in this test case.                                                                  |

# ✅ Using MagicMock to Simulate Login Behavior in Pytest

This section demonstrates how to use Python's `unittest.mock.MagicMock` to simulate the behavior of `authenticate_user` in our FastAPI project for testing login functionality without executing actual authentication logic. `MagicMock` extends the basic `Mock` class, providing additional functionality like automatic handling of magic methods (e.g., `__getitem__`, `__iter__`).

---

## 🧪 Test Case: `test_login_success_with_magicmock`


```python
#test_auth.py
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
```
- 🔍 Explanation

| Line                                                    | Description                                                                                                                                                                                    |
| ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mock_auth = MagicMock()`                               | Creates a `MagicMock` object. While `Mock` is used for simple mocking, `MagicMock` provides additional features such as automatic handling of magic methods (e.g., `__getitem__`, `__iter__`). |
| `mock_auth.return_value = User(...)`                    | This line configures the mock to return a predefined `User` object when the mock is called.                                                                                                    |
| `patch("app.routes.auth.authenticate_user", mock_auth)` | This replaces the real `authenticate_user` function in the `auth` module with our mock during the test execution.                                                                              |
| `client.post(...)`                                      | Simulates a POST request to the login endpoint of your FastAPI app, passing test credentials.                                                                                                  |
| `assert response.status_code == 200`                    | Asserts that the login was successful and the HTTP status code is 200.                                                                                                                         |
| `assert "access_token" in response.json()`              | Checks that the response includes an "access\_token", ensuring that JWT authentication was successful.                                                                                         |
| `assert mock_auth.call_count == 1`                      | Verifies that the `mock_auth` function was called exactly once, confirming that the mock was used as expected.                                                                                 |

## 🧰 Patching Objects and Methods

Patching allows replacing the real methods or attributes on objects during tests.
Example: Patching a Class Method
```python

# some_module.py
class DB:
    def connect(self):
        return "connected"

# test_module.py
from unittest.mock import patch
from some_module import DB

@patch.object(DB, "connect", return_value="mocked_connection")
def test_connect(mock_connect):
    db = DB()
    assert db.connect() == "mocked_connection"
    mock_connect.assert_called_once()
```

patch.object: Used to mock methods or attributes directly on an object.

It is useful when you want to replace a method on an actual instance of a class during tests.

## 🧬 Using Fixtures for Mocking in conftest.py

Fixtures in conftest.py help set up reusable mock objects across multiple test files.

Example: Fixture for Mocking
```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_api():
    mock = Mock()
    mock.fetch_user.return_value = {"username": "fixture_user"}
    return mock

# test_file.py
def test_with_fixture(mock_api):
    assert mock_api.fetch_user()["username"] == "fixture_user"
```
    
Fixtures in conftest.py allow you to create reusable mocks for multiple tests, making your tests cleaner and more maintainable.

The mock object (mock_api) is available across your test files as it is automatically injected by pytest.

## 🧾 Verifying Mock Calls

You can verify that mock methods were called with the expected arguments using assert_called_once and assert_called_with.
```python

from unittest.mock import Mock

mock_obj = Mock()
mock_obj.method("hello", key="value")

mock_obj.method.assert_called_once()
mock_obj.method.assert_called_with("hello", key="value")
```
assert_called_once: Ensures the mock method was called exactly once.

assert_called_with: Verifies the arguments with which the mock method was called.

## 🔥 Common Use Case: Mocking requests.get

Mocking external HTTP requests using requests.get is a common use case.

```python

import requests
from unittest.mock import patch

def get_status(url):
    res = requests.get(url)
    return res.status_code

@patch("requests.get")
def test_get_status(mock_get):
    mock_get.return_value.status_code = 200
    assert get_status("http://example.com") == 200
```

patch("requests.get"): Mocks the requests.get method, so no real HTTP requests are made during testing.

You can control the return value and simulate different HTTP responses.
