from pydantic import BaseModel
import typing as t
from .hall import Hall,HallCinema

class CinemaBase(BaseModel):
    name: str
    description: t.Union[str, None] = None
    
    class Config:
        from_attributes = True

class CinemaOut(CinemaBase):
    pass

class CinemaCreate(CinemaBase):
    is_active:bool
    
    class Config:
        from_attributes = True

class CinemaEdit(CinemaBase):
    name: t.Optional[str] = None
    description: t.Optional[str] = None

    class Config:
        from_attributes = True

class Cinema(CinemaBase):
    id: int
    is_active: bool
    halls: t.List[HallCinema] = None
    
    class Config:
        from_attributes = True