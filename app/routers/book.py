from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Response
import models, database
from schemas import book
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
import typing as t
from typing import Annotated, List

router = APIRouter(
    prefix="/books",
    tags=["Bookings"]
)

get_db = database.get_db

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/book_lists',response_model = book.Book,status_code = status.HTTP_200_OK)

async def fecth_bookings(db:db_dependency):

    return db.query(models.Book).all()

@router.get('/booking/{book_id}',response_model=book.Book,status_code = status.HTTP_200_OK)

async def fetch_booking(book_id:int,db:db_dependency):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with ID {book_id} not found")