import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Text, UniqueConstraint
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
    favorites = relationship("Favorite", back_populates="book")
    notification_requests = relationship("NotificationRequest", back_populates="book")

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
    favorites = relationship("Favorite", back_populates="user")
    notification_requests = relationship("NotificationRequest", back_populates="user")
    internal_messages = relationship("InternalMessage", back_populates="recipient")


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
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    # unique constraint on book_id and user_id
    __table_args__ = (UniqueConstraint('book_id', 'user_id', name='unique_book_user'),)


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    book = relationship("Book")
    user = relationship("User")
    # unique constraint on book_id and user_id
    __table_args__ = (UniqueConstraint('book_id', 'user_id', name='unique_book_fav_user'),)



class NotificationRequest(Base):
    __tablename__ = "notification_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    is_notified = Column(Boolean, default=False)

    user = relationship("User", back_populates="notification_requests")
    book = relationship("Book", back_populates="notification_requests")



class InternalMessage(Base):
    __tablename__ = "internal_messages"
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String, index=True)
    is_read = Column(Boolean, default=False)

    recipient = relationship("User", back_populates="internal_messages")
