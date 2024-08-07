from typing import Union
from pydantic import BaseModel
import typing as t
from .showing import Showing
from .seat import Seat


class HallBase(BaseModel):
    name: str
    description: Union[str, None] = None
    
    class Config:
        orm_mode = True

class HallOut(HallBase):
    pass

class HallCreate(HallBase):
    cinema_id:int
    is_active:bool
    
    class Config:
        from_attributes:True

class HallEdit(HallBase):
    name: t.Optional[str] = None
    description: t.Optional[str] = None

    class Config:
        orm_mode = True
        
class HallCinema(HallBase):
    id: int
    is_active: bool
    # seats: t.List[Seat] = None
    # showings: t.List[Showing] = None
    
    class Config:
        orm_mode = True

class Hall(HallBase):
    id: int
    cinema_id:int
    is_active: bool
    seats: t.List[Seat] = None
    showings: t.List[Showing] = None
    
    class Config:
        from_attributes = True