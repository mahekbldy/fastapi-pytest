
# 🔍 Pytest Fixtures: Scope, Lifecycle, and Call Order

## 🧭 1. Fixture Scope

Fixture **scope** controls how many times the fixture is invoked during a test session.

### 🔹 Available Scopes:

| Scope     | Lifespan                                 | When it's recreated              |
|-----------|------------------------------------------|----------------------------------|
| `function`| Default. One call per test function      | Every test                       |
| `class`   | Once per test class                      | Once per test class              |
| `module`  | Once per test module (file)              | Once per module                  |
| `package` | (new in Pytest 7.0) once per package     | Once per test package            |
| `session` | Once for the entire test session         | Once across the entire run       |

### 🔹 Example:

```python
import pytest

@pytest.fixture(scope="function")
def func_scope():
    print("Function scope fixture")
    return 1

@pytest.fixture(scope="module")
def mod_scope():
    print("Module scope fixture")
    return 2

@pytest.fixture(scope="session")
def sess_scope():
    print("Session scope fixture")
    return 3

def test_1(func_scope, mod_scope, sess_scope):
    pass

def test_2(func_scope, mod_scope, sess_scope):
    pass
```

**Output:**
```
Session scope fixture
Module scope fixture
Function scope fixture
Function scope fixture
```

---

## 🔁 2. Fixture Lifecycle

Lifecycle is the sequence:
- **Set up**: before `yield` or return
- **Tear down**: after `yield`

### Using `yield`:

```python
@pytest.fixture
def setup_teardown():
    print("Setup")
    yield
    print("Teardown")
```

---

## 📐 3. Order of Fixture Execution

### 🔹 Pytest resolves fixture order **bottom-up** (dependency chain), then executes **top-down**:

```python
@pytest.fixture
def db():
    print("Setting up DB")
    return {"db": "connected"   }

@pytest.fixture
def user(db):
    print("Creating user")
    return {"user": "Alice", "db": db}

def test_example(user):
    print("Running test")
```

**Execution Order:**
```
Setting up DB
Creating user
Running test
```

---

## ⛓️ 4. Chained Fixture Call Graph

```python
@pytest.fixture
def db():
    print("DB setup")
    yield
    print("DB teardown")

@pytest.fixture
def user(db):
    print("User setup")
    yield
    print("User teardown")

@pytest.fixture
def token(user):
    print("Token setup")
    yield
    print("Token teardown")

def test_token(token):
    print("Running test")
```

**Execution Order:**
```
DB setup
User setup
Token setup
Running test
Token teardown
User teardown
DB teardown
```

---

## 🌀 5. Fixture Teardown Order

- Teardowns happen in **reverse order** of setup.
- Like a stack: last-in, first-out (LIFO).

---

## 🔍 6. Visual: Setup & Teardown Timeline

```
[test_1]

SETUP: session_scope
SETUP: module_scope
SETUP: function_scope
→ RUN test_1
TEARDOWN: function_scope

[test_2]
SETUP: function_scope
→ RUN test_2
TEARDOWN: function_scope

TEARDOWN: module_scope
TEARDOWN: session_scope
```

---

## ✅ Summary

| Concept              | Details                                                                 |
|----------------------|-------------------------------------------------------------------------|
| Scope                | Controls how long a fixture lasts (`function`, `class`, `module`, etc.) |
| Lifecycle            | Controlled by `yield` with teardown after test completes                |
| Call Order           | Dependency-resolved; setup from bottom-up, teardown top-down            |
| Teardown Order       | Reverse of setup (last setup is first to teardown)                      |