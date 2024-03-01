import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from database import Base
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    year_of_publication = Column(Integer)
    category = Column(String)
    available_copies = Column(Integer, default=10)


    rentals = relationship("Rental", back_populates="book")
    reviews = relationship("Review", back_populates="book")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    rentals = relationship("Rental", back_populates="user")
    reviews = relationship("Review", back_populates="user")


class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rented_date = Column(DateTime, default=datetime.datetime.utcnow)
    return_date = Column(DateTime, default=None)
    is_returned = Column(Boolean, default=False)

    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    review = Column(String)
    rating = Column(Integer)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")