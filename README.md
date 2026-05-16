# Todo REST API

A complete Todo REST API built with FastAPI, SQLAlchemy, and JWT Authentication.

---

## Technologies Used

- **FastAPI** — API framework
- **SQLAlchemy** — Database ORM
- **SQLite** — Database
- **Pydantic** — Data validation
- **JWT (python-jose)** — Authentication tokens
- **Bcrypt (passlib)** — Password encryption
- **Pytest** — Unit testing

---

## Project Structure

```
todo_api/
├── app/
│   ├── main.py             # App entry point
│   ├── database.py         # Database connection and session
│   ├── auth.py             # JWT authentication and password hashing
│   ├── models/
│   │   └── models.py       # SQLAlchemy database models
│   ├── schemas/
│   │   └── schemas.py      # Pydantic schemas for validation
│   └── routers/
│       ├── users.py        # User registration and login endpoints
│       └── todos.py        # Todo CRUD endpoints
└── tests/
    └── test_api.py         # 16 unit tests
```

---

## Installation

### Step 1 — Install bcrypt
```bash
pip install bcrypt==4.0.1
```

### Step 2 — Install all dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Start the server
```bash
uvicorn app.main:app --reload
```

### Step 4 — Open in browser
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register a new user |
| POST | `/token` | Login and get JWT token |

### Todo Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/todos/` | Create a new todo |
| GET | `/todos/` | Get all todos (with filter and pagination) |
| GET | `/todos/{id}` | Get a specific todo by ID |
| PUT | `/todos/{id}` | Update a todo (full update) |
| PATCH | `/todos/{id}` | Update a todo (partial update) |
| DELETE | `/todos/{id}` | Delete a todo |

---

## Database Models

### User
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Unique email address |
| hashed_password | String | Encrypted password |
| created_at | DateTime | Account creation time |

### TodoItem
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Todo title |
| description | String | Todo description |
| completed | Boolean | Completion status |
| category | String | Todo category |
| user_id | Integer | Foreign key to User |
| created_at | DateTime | Creation time |
| updated_at | DateTime | Last update time |

---

## How to Use the API

### Step 1 — Register a User
```json
POST /users/
{
  "username": "yash",
  "email": "yash@example.com",
  "password": "mypassword123"
}
```

### Step 2 — Login and Get Token
```
POST /token
username: yash
password: mypassword123
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Step 3 — Create a Todo
```json
POST /todos/
Authorization: Bearer <your_token>

{
  "title": "My First Todo",
  "description": "FastAPI project completed",
  "category": "work"
}
```

### Step 4 — Get All Todos
```
GET /todos/
Authorization: Bearer <your_token>
```

Response:
```json
{
  "total": 1,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "title": "My First Todo",
      "description": "FastAPI project completed",
      "completed": false,
      "category": "work",
      "user_id": 1,
      "created_at": "2026-05-16T10:00:00"
    }
  ]
}
```

### Step 5 — Update a Todo
```json
PUT /todos/1
Authorization: Bearer <your_token>

{
  "title": "My First Todo",
  "completed": true
}
```

### Step 6 — Delete a Todo
```
DELETE /todos/1
Authorization: Bearer <your_token>
```

---

## Filtering and Pagination

Filter todos by status:
```
GET /todos/?completed=false
GET /todos/?completed=true
```

Filter todos by category:
```
GET /todos/?category=work
GET /todos/?category=personal
```

Pagination:
```
GET /todos/?page=1&page_size=5
GET /todos/?page=2&page_size=5
```

Combine filters:
```
GET /todos/?category=work&completed=false&page=1&page_size=10
```

---

## Running Tests

```bash
pytest tests/test_api.py -v
```

Expected output:
```
tests/test_api.py::TestAuth::test_register_user PASSED
tests/test_api.py::TestAuth::test_register_duplicate_username PASSED
tests/test_api.py::TestAuth::test_login_success PASSED
tests/test_api.py::TestAuth::test_login_wrong_password PASSED
tests/test_api.py::TestTodos::test_create_todo PASSED
tests/test_api.py::TestTodos::test_list_todos PASSED
tests/test_api.py::TestTodos::test_get_todo_by_id PASSED
tests/test_api.py::TestTodos::test_get_nonexistent_todo PASSED
tests/test_api.py::TestTodos::test_update_todo PASSED
tests/test_api.py::TestTodos::test_patch_todo PASSED
tests/test_api.py::TestTodos::test_delete_todo PASSED
tests/test_api.py::TestTodos::test_filter_by_completed PASSED
tests/test_api.py::TestTodos::test_filter_by_category PASSED
tests/test_api.py::TestTodos::test_pagination PASSED
tests/test_api.py::TestTodos::test_unauthorized_access PASSED
tests/test_api.py::TestTodos::test_cannot_access_other_users_todo PASSED

=============== 16 passed ===============
```

---

## Security Features

- Passwords are encrypted using **Bcrypt** before saving to database
- JWT tokens expire after **60 minutes**
- Every user can only access **their own todos**
- All endpoints (except register and login) require a valid JWT token
- Unauthorized access returns **401 error**
- Accessing another user's todo returns **404 error**

---

## API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI** — http://127.0.0.1:8000/docs
- **ReDoc** — http://127.0.0.1:8000/redoc

---

## Author

**Yash**
Web Development Internship Project
