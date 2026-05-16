from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── User Schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Auth Schemas ──────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Todo Schemas ──────────────────────────────────────────────
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    category: Optional[str] = "general"


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    category: Optional[str] = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    category: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedTodos(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[TodoResponse]
