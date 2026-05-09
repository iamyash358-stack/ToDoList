# FastAPI Todo API Project

A simple Todo REST API built using FastAPI, SQLAlchemy, SQLite, and JWT Authentication.

---

# Features

- User Registration
- User Login with JWT Authentication
- Create Todo
- Get All Todos
- Get Todo By ID
- Update Todo
- Delete Todo
- Filter Todos by Status and Category
- Pagination Support
- Swagger/OpenAPI Documentation
- Unit Testing using Pytest

---

# Technologies Used

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Passlib (Password Hashing)
- Pytest

---

# Project Structure

```bash
todo_api_project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── crud.py
│   ├── dependencies.py
│   └── routers/
│       ├── users.py
│       └── todos.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
└── README.md
