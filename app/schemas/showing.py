from pydantic import BaseModel
from datetime import datetime
import typing as t
from .book import Book


class ShowingBase(BaseModel):
    title: str
    start: datetime
    end: datetime
    
    class Config:
        orm_mode = True

class ShowingOut(ShowingBase):
    pass

class ShowingCreate(ShowingBase):
    hall_id: int
    movie_id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class ShowingEdit(ShowingBase):
    number: t.Optional[int] = None

    class Config:
        orm_mode = True

class Showing(ShowingBase):
    id: int
    hall_id: int
    movie_id: int
    is_active: bool
    books: t.List[Book] = None
    
    class Config:
        orm_mode = True