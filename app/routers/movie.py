from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Response
import models, database
from schemas import movie
from sqlalchemy.orm import Session
from typing import List
from core.config import settings
from oauth2 import get_current_active_superuser,get_current_user
from core.utils import hash

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

get_db = database.get_db

@router.post("/", response_model=movie.Movie, response_model_exclude_none=True)
async def create_movie(
    movie_instance: movie.MovieCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_superuser)
):
    db_name = db.query(models.Movie).filter(models.Movie.title == movie_instance.title).first()
    if db_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Movie with title '{movie_instance.title}' already exists"
        )
    
    db_movie = models.Movie(
        title=movie_instance.title,
        description=movie_instance.description,
        is_active=movie_instance.is_active,
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@router.get("/", response_model=List[movie.Movie], response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def movies_list(db: Session = Depends(get_db),  current_user = Depends(get_current_user)):
    db_movie = db.query(models.Movie).limit(100).all()
    return db_movie

@router.get("/{movie_id}", response_model=movie.Movie, status_code=status.HTTP_200_OK, response_model_exclude_none=True)
async def fetch_movie(movie_id: int, db: Session = Depends(get_db),  current_user = Depends(get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Movie with ID {movie_id} not found"
        )
    return db_movie

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: int, db: Session = Depends(get_db),  current_user = Depends(get_current_active_superuser)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id)
    if not db_movie.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Movie with ID {movie_id} not found"
        )
    db_movie.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Deleted"}
