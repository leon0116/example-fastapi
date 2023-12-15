from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
import sys

router = APIRouter(
      prefix="/posts",
      tags=['Posts']
)

# @router.get("/", response_model=list[schemas.PostOut])



#@router.get("/")
#def get_posts(db: Session = Depends(get_db), 
#              current_user: int = Depends(oauth2.get_current_user),
#              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#        #cursor.execute("""SELECT * FROM posts """)
#        #posts = cursor.fetchall()

#        posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
         #results = db.query(models.Post)



       # formatted_results = []
       # for post, vote_count in results:
       #               post_dict = post.__dict__
       #               post_dict["votes"] = vote_count
       #               formatted_results.append({"post": post_dict, "votes": vote_count})

         #return  results
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

      # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
      posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
      return posts






 



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
       #pydantic model 裡的post當成schema
       # sql
       #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                    #  (post.title, post.content, post.published))  
       #New_post = cursor.fetchone() 

       #conn.commit() 
       
       #
       # new_post =models.Post(title=post.title, content=post.content, published=post.published)  
       
       new_post = models.Post(owner_id=current_user.id, **post.dict())
       db.add(new_post)
       db.commit()
       db.refresh(new_post)

       return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
       #sql
       # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
       #post = cursor.fetchone()       
       post = db.query(models.Post).filter(models.Post.id == id).first()
       
       
       if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
       
       #限本人
       #  if post.owner_id != current_user.id:
       #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
       #                          detail="Not authorized to perform requested action")

       return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
      
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    #檢查刪除的人是不是本人
    if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

       
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate
                , db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    
   # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
   #               RETURNING *""", (post.title, post.content, post.published, str(id)))
    
   #update_post = cursor.fetchone()
   # conn.commit()   

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()    
    
    if post == None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")     
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    #如果有，把資料轉換成字典，然後加上id,然後取代原本的資料
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    #return{'data': post_dict}
    return post_query.first()