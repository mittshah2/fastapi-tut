from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=0, le=6)
    complete: bool


@app.get("/todo", status_code=200)
async def read_all(db: db_dependency):
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}", status_code=200)
async def read_all(db: db_dependency,
                   todo_id: int = Path(gt=0)):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    return todo


@app.post("/todo", status_code=201)
async def create_todo(db: db_dependency,
                      request: TodoRequest):
    todo_model = models.Todos(**request.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


@app.put("/todo/{todo_id}", status_code=204)
async def update_todo(db: db_dependency,
                      request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    todo_model.title = request.title
    todo_model.description = request.description
    todo_model.priority = request.priority
    todo_model.complete = request.complete

    db.add(todo_model)
    db.commit()


@app.delete("/todo/{todo_id}", status_code=204)
async def delete_todo(db: db_dependency,
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
