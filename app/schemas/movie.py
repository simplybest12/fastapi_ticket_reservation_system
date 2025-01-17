from typing import Union
from pydantic import BaseModel
from .showing import Showing 
import typing as t


class MovieBase(BaseModel):
    title: str
    description: Union[str, None] = None
    
    class Config:
        from_attributes = True

class MovieOut(MovieBase):
    pass

class MovieCreate(MovieBase):
    is_active: bool
    
    class Config:
        from_attributes = True

class MovieEdit(MovieBase):
    title: t.Optional[str] = None
    description: t.Optional[str] = None

    class Config:
        orm_mode = True

class Movie(MovieBase):
    id: int 
    is_active: bool
    showings: t.List[Showing] = None
    
    class Config:
        orm_mode = True