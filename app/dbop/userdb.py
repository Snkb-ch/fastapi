
from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException,status
from hashing import Hash

def create_user(request: schemas.UserCreate,db: Session):
    new_user = models.User(email=request.email,password=Hash.bcrypt(request.password), name=request.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    return user

def get_users(db: Session):
    users = db.query(models.User).all()
    return users

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    if user_update.email:
        db_user.email = user_update.email
    if user_update.name:
        db_user.name = user_update.name
    if user_update.password:
        db_user.password = Hash.bcrypt(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db, user_id):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


def promote_user(db, user_id):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.is_admin = True
    db.commit()
    db.refresh(db_user)
    return db_user

