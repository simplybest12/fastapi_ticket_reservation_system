from fastapi import FastAPI, APIRouter, HTTPException, status, Depends, Response
import models, database
from schemas import seat
from sqlalchemy.orm import Session
from typing import List,Annotated
from core.config import settings
from core.utils import hash

router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
)

get_db = database.get_db

db_dependency= Annotated[Session,Depends(get_db)]

@router.post('/seat',response_model = seat.Seat, response_model_exclude_none=True)

async def create_seat(db:db_dependency,seat_instance:seat.SeatCreate):
    db_seat = models.Seat(
        number = seat_instance.number,
        row = seat_instance.row,
        hall_id = seat_instance.hall_id,
        is_active = seat_instance.is_active
    )
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

@router.get("/", response_model=List[seat.Seat], response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def seats_list(db: Session = Depends(get_db)):
    db_seat = db.query(models.Seat).limit(100).all()
    return db_seat

@router.get("/{seat_id}", response_model=seat.Seat, status_code=status.HTTP_200_OK, response_model_exclude_none=True)
async def fetch_seat(seat_id: int, db: Session = Depends(get_db)):
    db_seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not db_seat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"seat with ID {seat_id} not found"
        )
    return db_seat

@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_seat(seat_id: int, db: Session = Depends(get_db)):
    db_seat = db.query(models.Seat).filter(models.Seat.id == seat_id)
    if not db_seat.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"seat with ID {seat_id} not found"
        )
    db_seat.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Deleted"}
