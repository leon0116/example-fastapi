from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# def find_post(id):
#        for p in my_posts:
#               if p["id"] == id:
#                      return p


# def find_index_post(id):
#        for i, p in enumerate(my_posts):
#               if p['id'] == id:
#                      return i



@app.get("/")
def root():
       return {"message": "123"}

# test sqlachemy
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
     
#       posts = db.query(models.Post).all()
#       return{"data": posts}

      