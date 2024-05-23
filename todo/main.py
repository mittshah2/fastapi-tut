from fastapi import FastAPI
from todo.routers import auth, todo, admin
from todo import models, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
