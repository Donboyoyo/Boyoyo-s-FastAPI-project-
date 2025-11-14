from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags=['Users']
)



#User registration path operation
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.GeneratedResponse)
def create_user(new_user: schemas.GenerateUser, db: Session = Depends(get_db)):

    #hash the password, which can be retrieved from new_user.password
    hashed_pasword = utils.hash(new_user.password)
    new_user.password = hashed_pasword

    user_login = models.User(**new_user.model_dump())
    db.add(user_login)
    db.commit()
    db.refresh(user_login)

    return user_login


# Path operation to get user by id 
@router.get("/{id}", response_model= schemas.GeneratedResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {id} does not exist")

    return user