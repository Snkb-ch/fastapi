import datetime

from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException,status

def get_books(db: Session, current_user: schemas.User = None):
    books = db.query(models.Book).all()


    # add average rating
    for book in books:
        book.average_rating = average_rating(db, book.id)
        if current_user:
            favorite_exists = db.query(models.Favorite).filter(models.Favorite.book_id == book.id, models.Favorite.user_id == current_user.user_id).first() is not None
            book.favorite = favorite_exists




    return books

def average_rating(db: Session, book_id: int):
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    if not reviews:
        return 0
    total = 0
    for review in reviews:
        total += review.rating
    total =round(total/len(reviews), 2)
    return total
def get_book(db: Session, id: int, current_user: schemas.User = None):
    book = db.query(models.Book).filter(models.Book.id == id).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {id} not found")

    book.average_rating = average_rating(db, book.id)
    # return 3 recent reviews
    reviews = db.query(models.Review).filter(models.Review.book_id == id).order_by(models.Review.id.desc()).limit(3).all()
    if current_user:
        favorite = db.query(models.Favorite).filter(models.Favorite.book_id == book.id, models.Favorite.user_id == current_user.user_id).first() is not None
        book.favorite = favorite
    # list of dictionaries
    book.topreviews = []
    for review in reviews:
        book.topreviews.append({"rating": review.rating, "comment": review.comment, "user": review.user.name})





    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id {id} not found")
    return book
def search_books(db, title: str = None, author: str = None, year_of_publication: int = None, category: str = None, favorite: bool = False, current_user: schemas.User = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title == title)
    if author:
        query = query.filter(models.Book.author == author)
    if year_of_publication:
        query = query.filter(models.Book.year == year_of_publication)
    if category:
        query = query.filter(models.Book.category == category)
    if favorite:
        query = query.filter(models.Favorite.user_id == current_user.user_id, models.Favorite.book_id == models.Book.id)
    result = []
    for book in query:
        book = get_book(db, book.id, current_user)
        result.append(book)


    return result

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

    new_book = models.Book(**request.model_dump())

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
    for key, value in request.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_review(db, book_id, request, current_user):
    db_review = models.Review(**request.dict(), book_id=book_id, user_id=current_user.user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db, book_id):
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    for review in reviews:
        user = db.query(models.User).filter(models.User.id == review.user_id).first()
        review.username = user.name

    return reviews


def update_review(db, book_id, review_id, request, current_user):
    db_review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.book_id == book_id, models.Review.user_id == current_user.user_id).first()
    if not db_review:
        return None
    for key, value in request.dict().items():
        setattr(db_review, key, value)
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db, book_id, review_id, current_user):
    db_review = db.query(models.Review).filter(models.Review.id == review_id, models.Review.book_id == book_id, models.Review.user_id == current_user.user_id).first()
    if not db_review:
        return None
    db.delete(db_review)
    db.commit()
    return db_review


def create_favorite(db, book_id, current_user):
    db_fav = models.Favorite(book_id=book_id, user_id=current_user.user_id)
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav


def get_favorites(db, current_user):
    dv_favs = db.query(models.Favorite).filter(models.Favorite,user_id = current_user.user_id).all()
    return dv_favs


def delete_favorite(db, book_id, current_user):
    db_fav = db.query(models.Favorite).filter(models.Favorite.book_id == book_id, models.Favorite.user_id == current_user.user_id).first()
    if not db_fav:
        return None
    db.delete(db_fav)
    db.commit()
    return db_fav


def create_notification(db, book_id, current_user):
    existing_request = db.query(models.NotificationRequest).filter_by(user_id=current_user.user_id, book_id = book_id,
                                                                      is_notified=False).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="You have already requested a notification for this book.")
    book = db.query(models.Book).filter_by(id=book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    if book.available_copies > 0:
        raise HTTPException(status_code=400, detail="Book is already available.")
    notification_request = models.NotificationRequest(user_id=current_user.user_id, book_id=book_id)
    db.add(notification_request)
    db.commit()
    db.refresh(notification_request)
    return notification_request


