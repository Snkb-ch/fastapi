
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class UserUpdate(UserBase):
    name :Optional[str]  = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class BookBase(BaseModel):
    title: str
    author: str
    year_of_publication: int
    category: str

class BookSearch(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    year_of_publication: Optional[int] = None
    category: Optional[str] = None


class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int


    class Config:
        orm_mode = True

class RentalBase(BaseModel):
    user_id: int
    book_id: int

class RentalCreate(RentalBase):
    rental_date: date
    return_date: Optional[date] = None

class Rental(RentalBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True