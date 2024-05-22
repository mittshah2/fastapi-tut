from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"hello": f"Hello {name}"}


# /hello?name=mitt&disp=false
@app.get("/hello")
async def say_hello(name: str, disp: bool = True):
    if not disp:
        name = ""
    return {"hello": f"Hello {name}"}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None


# change port to 3000 (run the application -> python main.py)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=3000)
