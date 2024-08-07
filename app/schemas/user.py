from pydantic import BaseModel
import typing as t
from .book import Book


class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None

class UserOut(UserBase):
    pass

class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True
        
class User(UserBase):
    id: int
    books: t.List[Book] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email:str
    password:str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: t.Optional[str] = None
    permissions: str = "user"