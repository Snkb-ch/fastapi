from typing import List, Optional
from fastapi import APIRouter,Depends,status,HTTPException
import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from dbop import bookdb

router = APIRouter(
    prefix="/books",
    tags=['Books']
)

get_db = database.get_db


@router.get('/', response_model=List[schemas.Book])
async def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = bookdb.get_books(db)
    return books



# @router.post('/search', response_model=List[schemas.Book])
# async def search_books(request: schemas.BookSearch, db: Session = Depends(get_db)):
#     books = bookdb.search_books(db, title=request.title, author=request.author, year_of_publication=request.year_of_publication, category=request.category)
#     return books
@router.get('/search', response_model=List[schemas.Book])
async def search_books(title: Optional[str] = None, author: Optional[str] = None, year_of_publication: Optional[int] = None, category: Optional[str] = None, db: Session = Depends(get_db)):
    books = bookdb.search_books(db, title=title, author=author, year_of_publication=year_of_publication, category=category)
    return books
@router.get('/{book_id}', response_model=schemas.Book)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = bookdb.get_book(db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
@router.post('/rent/{book_id}', response_model=schemas.Book)
async def rent_book(book_id: int, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    db_book = bookdb.rent_book(db, book_id, current_user)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post('/return/{book_id}', response_model=schemas.Book)
async def return_book(book_id: int, current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    db_book = bookdb.return_book(db, book_id, current_user)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


# if admin than create, delete, update books

@router.post('/', response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(request: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    db_book = bookdb.create_book(request, db)
    return db_book

@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    db_book = bookdb.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put('/{book_id}', response_model=schemas.Book)
async def update_book(book_id: int, request: schemas.BookCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="You are not admin")
    db_book = bookdb.update_book(db, book_id, request)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


