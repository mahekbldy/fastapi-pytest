# 🧪 FastAPI + Pytest Example Project

This project demonstrates a full-featured FastAPI application with JWT-based login, user filtering, and comprehensive Pytest test coverage — all without a real database. Instead, user data is stored in a JSON file for simplicity and educational purposes.

---

## 🗂️ Project Structure

```
app/
├── __init__.py
├── main.py              # Entry point for FastAPI app
├── models.py            # Load users from JSON
├── schemas.py           # Pydantic models
├── auth.py              # Authentication logic (login, JWT)
├── dependencies.py      # Reusable FastAPI dependencies
├── user_data.json       # Pre-populated users
└── routes/
    ├── __init__.py
    ├── auth.py          # /auth/login route
    └── users.py         # /users route

tests/
├── __init__.py
├── conftest.py          # Fixtures, test config
├── test_auth.py         # Tests for login
└── test_users.py        # Tests for user listing

```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn python-jose[cryptography] pytest
```

### 2. Run the Server

```bash
python app/main.py
```

Visit Swagger docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Authentication

Login with one of the pre-populated users in `user_data.json`:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

You’ll get a JWT token that includes user `id`, `name`, and `role`. Use it in the `/users` endpoint to access protected data.

---

## 🔍 API Endpoints

| Method | Endpoint       | Description                        |
|--------|----------------|------------------------------------|
| POST   | /auth/login    | Get JWT token                      |
| GET    | /users         | List all users with filters        |

Query parameters for `/users`:
- `id` (int)
- `name` (str)
- `role` (str)

Example:

```
GET /users?role=admin&name=ali
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

Includes tests for:
- ✅ Login success and failure
- ✅ JWT token generation
- ✅ Authenticated access
- ✅ User filtering by ID, name, role
- ✅ Unauthorized access

Fixtures used:
- `client` for FastAPI test client
- `mock_users` for simulated DB
- `token` for authorized requests

---

## ✅ Concepts Covered

- FastAPI routing & dependency injection
- JWT authentication (`python-jose`)
- Pydantic schemas and typing
- Test structure with `pytest`
- `conftest.py` and reusable fixtures
- Parametrized and isolated tests
- Swagger docs (`/docs`)

---

## 📁 Sample User Credentials

| Username | Password  | Role   |
|----------|-----------|--------|
| admin    | admin123  | admin  |
| john     | johnpass  | user   |
| jane     | janepass  | user   |
| bob      | bobpass   | user   |
| eva      | evapass   | admin  |

(And more in `user_data.json`...)

---

Happy Testing! 💡