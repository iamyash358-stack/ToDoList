from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, todos

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo API",
    description="A full-featured Todo REST API with JWT authentication",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(todos.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Todo API is running!", "docs": "/docs"}
