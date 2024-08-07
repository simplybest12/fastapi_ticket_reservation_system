from fastapi import FastAPI,APIRouter,HTTPException,status,Depends, Response
import models,database
from schemas import hall
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
from oauth2 import get_current_active_superuser,get_current_user

import typing as t
from typing import Annotated,List

router = APIRouter(
    prefix = "/hall",
    tags = ["Halls"]
)

get_db = database.get_db

db_dependency= Annotated[Session,Depends(get_db)]

@router.post("/halls", response_model=hall.Hall, response_model_exclude_none=True)

async def create_hall(hall_instance:hall.HallCreate,db:db_dependency,  current_user = Depends(get_current_active_superuser)):
    db_cinema = db.query(models.Cinema).filter(models.Cinema.id == hall_instance.cinema_id).first()
    if not db_cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cinema with ID {hall_instance.cinema_id} not found")
    
    db_name = db.query(models.Hall).filter(models.Hall.name == hall_instance.name).first()
    if  db_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cinema with Name {hall_instance.name} already exist")
    
    db_hall = models.Hall(
        name = hall_instance.name,
        description = hall_instance.description,
        cinema_id = hall_instance.cinema_id,
        is_active = hall_instance.is_active,
    )
    db.add(db_hall)
    db.commit()
    db.refresh(db_hall)
    return db_hall


@router.get("/halls", 
            response_model=t.List[hall.Hall], 
            response_model_exclude_none=True,
            status_code = status.HTTP_200_OK)

async def halls_list(db:db_dependency,  current_user = Depends(get_current_user)):
    db_halls = db.query(models.Hall).limit(100).all()
    return db_halls

@router.get("/hall/{hall_id}",
            response_model = hall.Hall,
            status_code = status.HTTP_200_OK
            )

async def fetch_hall(hall_id:int,db:db_dependency, current_user = Depends(get_current_user)):
    db_hall = db.query(models.Hall).filter(models.Hall.id == hall_id).first()
    if not db_hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hall with ID {hall_id} not found")
    return db_hall  

@router.delete('/hall_delete/{hall_id}',
                status_code = status.HTTP_204_NO_CONTENT
               )

async def delete_hall(hall_id:int,db:db_dependency, current_user = Depends(get_current_active_superuser)):
    db_hall = db.query(models.Hall).filter(models.Hall.id == hall_id)
    if not db_hall.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hall with ID {         hall_id} not found")
    db_hall.delete(synchronize_session = False)
    db.commit()
    return {"Message" : "Deleted"}
    
    