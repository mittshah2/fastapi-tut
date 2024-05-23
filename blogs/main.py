from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models, database

app = FastAPI()
models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
async def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    db_blog = models.Blog(title=request.title, body=request.body)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.get("/blog", status_code=status.HTTP_201_CREATED)
async def get_blogs_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}")
def get_blogs_by_id(id: int, response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter_by(id=id).first()
    if not blogs:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with id {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blogs


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_blogs(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter_by(id=id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.__dict__)
    db.commit()
    return request


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    # status code 204 doesn't allow to return anything