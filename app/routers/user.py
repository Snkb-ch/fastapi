from typing import List

from fastapi import APIRouter, HTTPException
import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status

import oauth2
from dbop import  userdb

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = userdb.create_user(request, db)
    return db_user

# only admin can see all users
@router.get('/', response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    users = userdb.get_users(db)
    return users

# user can only see his/her own details or admin can see all details
@router.get('/{user_id}', response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.user_id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You can only see your own details")
    db_user = userdb.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# user can update only his/her own details
@router.put('/{user_id}', response_model=schemas.User)
async def update_user(user_id: int, request: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=400, detail="You can only update your own details")
    db_user = userdb.update_user(db, user_id, request)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# only admin can delete users

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    db_user = userdb.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
# admin can promote user to admin

@router.put('/promote/{user_id}', response_model=schemas.User)
async def promote_user(user_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    db_user = userdb.promote_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

