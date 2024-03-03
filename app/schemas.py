
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

    class ConfigDict:
        from_attributes = True

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
    favorite : Optional[bool] = False


class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    average_rating: Optional[float] = None
    available_copies: Optional[int] = None
    topreviews: Optional[list] = None
    favorite: Optional[bool] = None


    class ConfigDict:
        from_attributes = True

class RentalBase(BaseModel):
    user_id: int
    book_id: int

class RentalCreate(RentalBase):
    rental_date: date
    return_date: Optional[date] = None

class Rental(RentalBase):
    id: int

    class ConfigDict:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    is_admin: Optional[bool] = None

    class ConfigDict:
        from_attributes = True


class ReviewBase(BaseModel):
    rating: float
    comment: Optional[str] = None



class ReviewCreate(ReviewBase):

    pass

class Review(ReviewBase):
    id: int
    username: str

    class ConfigDict:
        from_attributes = True


class ReviewUpdate(ReviewBase):
    rating: Optional[float] = None
    comment: Optional[str] = None

    class ConfigDict:
        from_attributes = True


class FavoriteBase(BaseModel):
    user_id: int
    book_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int

    class ConfigDict:
        from_attributes = True


class FavoriteDelete(FavoriteBase):
    pass




class NotificationRequestCreate(BaseModel):
    pass

class NotificationRequest(BaseModel):
    id: int
    user_id: int
    book_id: int
    is_notified: Optional[bool] = False

    class ConfigDict:
        from_attributes = True
class InternalMessageCreate(BaseModel):
    recipient_id: int
    message: str

class InternalMessage(BaseModel):
    id: int
    recipient_id: int
    message: str
    is_read: Optional[bool] = False

    class ConfigDict:
        from_attributes = True
