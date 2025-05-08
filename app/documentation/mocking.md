# 🎭 Mocking in Pytest using `unittest.mock` – Complete Guide

---

## 🔍 What is Mocking?

**Mocking** is the process of replacing real objects or functions with **fake (mocked) versions** to isolate behavior during testing.

- Use when you don’t want to call actual dependencies (e.g., database, API).
- Common for testing in isolation, verifying calls, and controlling return values.

---

## 📦 Tools Used

- Python’s built-in `unittest.mock`
- Key functions: `@patch`, `Mock`, `MagicMock`, `patch.object`, `patch.dict`

---

## 🔧 Basic Example with `patch`

```python
from unittest.mock import patch

# code.py
def get_username(api):
    return api.fetch_user()["username"]

# test_code.py
@patch("code.api.fetch_user")
def test_get_username(mock_fetch):
    mock_fetch.return_value = {"username": "mocked_user"}
    assert get_username(api="ignored") == "mocked_user"
```

## 🧪 Using Mock and MagicMock

Mock and MagicMock are used to create mock objects that simulate real objects or behaviors.
Mock
```python
from unittest.mock import Mock

mock_api = Mock()
mock_api.fetch_user.return_value = {"username": "test"}

assert mock_api.fetch_user()["username"] == "test"
```

Mock is a general-purpose mock object used to simulate objects, like API calls or database connections.

You can define return values for methods, like fetch_user.return_value.

## MagicMock

```python
from unittest.mock import MagicMock

mock_list = MagicMock()
mock_list.__len__.return_value = 5

assert len(mock_list) == 5
```
MagicMock is a subclass of Mock that can also handle special methods like __len__, __getitem__, etc.

It is useful when you need to mock more complex behaviors, such as operator overloading or special methods.

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
