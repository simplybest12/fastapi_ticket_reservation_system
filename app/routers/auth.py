from fastapi import FastAPI,APIRouter,HTTPException,status,Depends, Response
import models,database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schemas import user
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
import oauth2
import typing as t
from typing import Annotated,List

router = APIRouter(

    tags = ["Authentication"]
)

get_db = database.get_db

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/login')

def login(user_credential:OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm is replace of schema model which takes input in form of password and username
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not hash.Hash.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
        
    
    
    #create a token
    
    access_token = oauth2.create_access_token(data = {"user_email":user.email,"permissions":permissions})
    # return a token
    return {"access_token":access_token,"token_type":"bearer"}