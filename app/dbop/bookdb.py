import datetime

from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException,status

def get_books(db: Session):
    books = db.query(models.Book).all()
    return books

def get_book(db: Session, id: int):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {id} not found")
    return book
def search_books(db, title: str = None, author: str = None, year_of_publication: int = None, category: str = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title == title)
    if author:
        query = query.filter(models.Book.author == author)
    if year_of_publication:
        query = query.filter(models.Book.year == year_of_publication)
    if category:
        query = query.filter(models.Book.category == category)
    return query.all()

def rent_book(db: Session, book_id: int, user: schemas.User):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    if db_book.available_copies < 1:
        raise HTTPException(status_code=400, detail="Book not available")
    db_book.available_copies -= 1
    db.commit()
    db.refresh(db_book)

    db_rental = models.Rental(book_id=book_id, user_id=user.user_id)
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)

    return db_book

def return_book(db: Session, book_id: int, user: schemas.User):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db_book.available_copies += 1
    db.commit()
    db.refresh(db_book)

    rental = db.query(models.Rental).filter(models.Rental.book_id == book_id, models.Rental.user_id == user.user_id, models.Rental.is_returned == False).first()
    if not rental:
        raise HTTPException(status_code=400, detail="Book not rented by user")
    rental.is_returned = True
    rental.return_date = datetime.datetime.utcnow()
    db.commit()
    db.refresh(rental)
    return db_book


def create_book(request, db):
    new_book = models.Book(**request.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(db, book_id):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book


def update_book(db, book_id, request):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    for key, value in request.dict().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book