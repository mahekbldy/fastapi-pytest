
# 📁 `conftest.py` in Pytest – In-Depth Guide

---

## 🧾 What is `conftest.py`?

- A special file where you **define shared fixtures** for **multiple test files**.
- Automatically discovered by Pytest.
- No need to import fixtures explicitly in test modules.

---

## ✅ Why Use `conftest.py`?

| Benefit                        | Explanation                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Centralized setup             | Define common fixtures in one place                                        |
| Reusability                   | Used across multiple test files                                            |
| Cleaner test files            | No clutter of fixture definitions                                          |
| Auto-discovery by Pytest      | Pytest loads fixtures automatically                                        |

---

## 📂 Directory Structure Example

```
tests/
├── conftest.py          # Shared fixtures
├── test_auth.py
├── test_user.py
```

---

## 🧪 Example: Using `conftest.py`

### `conftest.py`
```python
import pytest

# Fixture to create a JWT token for a user
@pytest.fixture
def token(mock_users):
    user = mock_users[0]  # Use the first user as a default (admin)
    return create_access_token(user)

```

### `test_user.py`
```python
def test_filter_by_id(client, token):
    """Test filtering users by ID."""
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/?id=1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1

```

- `token` is **automatically injected** — no need to import from `conftest.py`.

---

## 🔁 Scope Works with `conftest.py` Too

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def db_connection():
    print("Connecting to DB")
    yield {"status": "connected"}
    print("Disconnecting from DB")
```

### `test_db.py`
```python
def test_connection(db_connection):
    assert db_connection["status"] == "connected"
```

---

## 🚫 What Not to Do

- ❌ Don’t import `conftest.py` directly
  ```python
  # WRONG:
  from tests.conftest import sample_user
  ```

- ✅ Pytest will automatically find and use fixtures defined in it.

---

## 🧬 Multiple `conftest.py` Files

You can have one `conftest.py` per package:

```
tests/
├── conftest.py                # Global fixtures
├── api/
│   ├── conftest.py            # API-specific fixtures
│   └── test_api_routes.py
├── models/
│   ├── test_models.py
```

- Pytest walks up the directory tree to find matching fixtures.
- Local `conftest.py` takes precedence over global.

---

## 🎯 Best Practices

| Practice                           | Reason                                                 |
|------------------------------------|--------------------------------------------------------|
| Keep it minimal                    | Only shared fixtures, not test data                    |
| Use consistent names               | Easy to identify in test functions                     |
| Use scoping to optimize performance| Avoid reconnecting or resetting for every test         |
| Group per domain if needed         | E.g., API vs DB vs Auth fixtures                       |

---

## 🧠 Summary

- `conftest.py` is for **shared, auto-discovered** fixtures.
- Fixtures can have **scopes**, **dependencies**, and be reused across tests.
- Organize cleanly for scalable testing infrastructure.



---

## 🧭 Local vs Global `conftest.py` – Precedence

### ✅ Yes, Local `conftest.py` Takes Precedence

When Pytest resolves fixtures, it starts searching from the **directory of the test file**, and moves **upwards** through the directory tree.

If multiple `conftest.py` files define a fixture with the same name, the **closest one wins**.

### 📂 Example Directory Structure

```
tests/
├── conftest.py               # Global fixture
├── api/
│   ├── conftest.py           # Local fixture (overrides global)
│   └── test_api_routes.py
```

### 🔧 `tests/conftest.py` (Global)

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Alice", "role": "global"}
```

### 🔧 `tests/api/conftest.py` (Local)

```python
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Bob", "role": "local"}
```

### 🧪 `tests/api/test_api_routes.py`

```python
def test_user(sample_user):
    assert sample_user["role"] == "local"
```

### ✅ Result

Even though `sample_user` is defined in both conftest files, the **local fixture** in `tests/api/conftest.py` is used.

This is useful when:
- You want different setup for a specific subset of tests.
- You want to override shared fixtures temporarily.

---

## 🔁 Fixture Resolution Order

1. Local `conftest.py` (same directory as the test)
2. Parent directories’ `conftest.py` files (searched upward)
3. Fixtures in imported modules (least preferred)

---

## 💡 Tip

Avoid fixture name conflicts unless you intentionally want to override a fixture in a subdirectory.
