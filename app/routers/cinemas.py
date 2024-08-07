from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Response
import models, database
from schemas import cinemas
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
import typing as t
from typing import Annotated, List

router = APIRouter(
    prefix="/cinemas",
    tags=["Cinemas"]
)

get_db = database.get_db

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/cinemas", response_model=cinemas.Cinema, response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def create_cinema(cinema_instance: cinemas.CinemaCreate, db: db_dependency):
    db_cinema = models.Cinema(**cinema_instance.dict())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema

@router.get('/cinema_list', response_model=List[cinemas.Cinema], status_code=status.HTTP_200_OK, response_model_exclude_none=True)
async def cinema_list(db: db_dependency):
    db_cinemas = db.query(models.Cinema).limit(10).all()
    return db_cinemas

@router.get('/cinema/{cinema_id}', response_model=cinemas.Cinema, status_code=status.HTTP_200_OK,response_model_exclude_none=True)
async def fetch_cinema(cinema_id: int, db: db_dependency):
    db_cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not db_cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cinema with ID {cinema_id} not found")
    return db_cinema

@router.put("/cinema_edit/{cinema_id}", response_model=cinemas.Cinema, response_model_exclude_none=True, status_code=status.HTTP_202_ACCEPTED)
async def cinema_edit(cinema_id: int, cinema: cinemas.CinemaEdit, db: db_dependency):
    db_cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not db_cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cinema with ID {cinema_id} not found")
    update_data = cinema.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cinema, key, value)

    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return db_cinema

@router.delete("/cinemas/{cinema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cinema_delete(cinema_id: int, db: db_dependency):
    db_cinema = db.query(models.Cinema).filter(models.Cinema.id == cinema_id).first()
    if not db_cinema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cinema with ID {cinema_id} not found")
    
    db.delete(db_cinema)
    db.commit()
    return {"Message":"Deleted"}  # Ensure no content is returned
