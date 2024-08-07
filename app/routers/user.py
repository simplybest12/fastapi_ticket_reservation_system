from fastapi import FastAPI,APIRouter,HTTPException,status,Depends, Response
import models,database
from schemas import user
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
from oauth2 import get_current_active_superuser,get_current_user


import typing as t
from typing import Annotated,List

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

get_db = database.get_db

db_dependency= Annotated[Session,Depends(get_db)]

@router.post("/",status_code = status.HTTP_201_CREATED,response_model = user.User)

async def user_create(user_instance:user.UserCreate,db:db_dependency,):
    user = db.query(models.User).filter(models.User.email==user_instance.email).first();
    if user:
        return False 
    hashed_password = hash.Hash.bcrypt(user_instance.password)
    user_instance.password = hashed_password
    db_user = models.User(**user_instance.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get('/users',
            response_model = t.List[user.User],
            response_model_exclude_none=True,
            status_code = status.HTTP_200_OK,
            
            )

async def user_lists(db:db_dependency):
    return db.query(models.User).limit(100).all()

@router.get(
    "/users/{user_id}",
    response_model=user.User,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)

async def user_detail(user_id:int,db:db_dependency,current_user=Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return db_user


@router.put(
    "/users/{user_id}",
    response_model=user.User,
    response_model_exclude_none=True,
    status_code=status.HTTP_202_ACCEPTED,
    
    
)
async def update_user(user_id: int, user: user.User, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)

async def delete_user(user_id:int,db:db_dependency,current_user=Depends(get_current_active_superuser)):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    
    if not db_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message":"user deleted"}
