from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


# Getting all posts 
@router.get("/", response_model= List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    # cursor.execute(""" SELECT * FROM newpost""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return posts




# Creating a post 
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):

    # cursor.execute(""" INSERT INTO newpost (title, content) VALUES (%s, %s) RETURNING * """, 
    #                (new_post.title, new_post.content))
    # created_post = cursor.fetchone()
    # conn.commit()                         # this is the line of code that pushes our created post into our table
     
    print(current_user.id)
    created_post = models.Post(owner_id = current_user.id, **new_post.model_dump())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)  # created_post is not a dictionary, it is a sqlalchemy model
    
    return created_post





# To get one post 
@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):

    # cursor.execute(""" SELECT * FROM newpost WHERE id = %s""", (str(id),))
    # one_post = cursor.fetchone()

    # one_post = db.query(models.Post).filter(models.Post.id == id).first()

    one_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first()


    if not one_post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found at all in this place")
    return one_post

# Deleting a post 
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM newpost WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()


    post_to_delete = db.query(models.Post).filter(models.Post.id == id)


    post = post_to_delete.first()

    if post == None :
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Updating a post with put 
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE newpost SET title = %s, content = %s WHERE id = %s RETURNING *""", 
    #                (updated_post.title, updated_post.content, str(id),))
    # final_update = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    final_update = post_query.first()

    if final_update == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist!")


    if final_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
