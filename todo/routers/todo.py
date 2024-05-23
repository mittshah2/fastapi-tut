from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from todo import database
from todo.routers.auth import get_user
from todo.models import Todos

router = APIRouter()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=0, le=6)
    complete: bool


@router.get("/todo", status_code=200)
async def read_all(db: db_dependency,
                   user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401,
                            detail='Authentication failed')
    return db.query(Todos).filter(Todos.owner_id == user['id']).all()


@router.get("/todo/{todo_id}", status_code=200)
async def read_all(db: db_dependency,
                   user: user_dependency,
                   todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,
                            detail='Authentication failed')
    todo = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user['id']).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo


@router.post("/todo", status_code=201)
async def create_todo(db: db_dependency,
                      user: user_dependency,
                      request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,
                            detail='Authentication failed')
    todo_model = Todos(**request.model_dump(), owner_id=user['id'])
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@router.put("/todo/{todo_id}", status_code=204)
async def update_todo(db: db_dependency,
                      user: user_dependency,
                      request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,
                            detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user['id']).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    todo_model.title = request.title
    todo_model.description = request.description
    todo_model.priority = request.priority
    todo_model.complete = request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(db: db_dependency,
                      user: user_dependency,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,
                            detail='Authentication failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id). \
        filter(Todos.owner_id == user['id']).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user['id']).delete()
    db.commit()
