from pydantic import BaseModel
from .book import Book 
import typing as t


class SeatBase(BaseModel):
    number: int
    
    class Config:
        orm_mode = True

class SeatOut(SeatBase):
    pass

class SeatCreate(SeatBase):
    row:str
    hall_id: int
    is_active: bool

class SeatEdit(SeatBase):
    number: t.Optional[int] = None

    class Config:
        orm_mode = True

class Seat(SeatBase):
    id: int
    hall_id: int
    row:str
    number:int
    is_active: bool
    books: t.List[Book] = None
    
    class Config:
        orm_mode = True