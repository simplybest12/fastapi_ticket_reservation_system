from fastapi import FastAPI, APIRouter, HTTPException, status, Depends , Response
import models, database
from schemas import showing
from sqlalchemy.orm import Session
from core.config import settings
from core.utils import hash
import typing as t
from typing import Annotated, List

router = APIRouter(
    prefix="/showing",
    tags=["Showing"]
)

get_db = database.get_db

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/showings", response_model=showing.Showing, response_model_exclude_none=True)
async def showing_create(showing: showing.ShowingCreate,db:db_dependency):
    db_show = models.Showing(
        title = showing.title,
        start = showing.start,
        end = showing.end,
        hall_id = showing.hall_id,
        movie_id = showing.movie_id,
        is_active = showing.is_active,
    )
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show

@router.get('/showing_list',response_model = t.List[showing.Showing] , response_model_exclude_none = True
            ,status_code = status.HTTP_200_OK
            )

async def fetch_shows(db:db_dependency):
    db_shows = db.query(models.Showing).limit(10).all()
    # response.headers["Content-Range"] = f"0-9/{len(db_shows)}"
    return db_shows


@router.get('/show/{show_id}',response_model= showing.Showing, response_model_exclude_none = True
            ,status_code = status.HTTP_200_OK)

async def fetch_show(show_id:int,db:db_dependency):
    db_show = db.query(models.Showing).filter(models.Showing.id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Show with ID {show_id} not found")
    return db_show

@router.delete('/show_del/{show_id}',status_code = status.HTTP_204_NO_CONTENT)

async def delete_showing(db: db_dependency, show_id: int):
    showing = db.query(models.Showing).filter(models.Showing.id == show_id)
    if not showing.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="showing not found")
    showing.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Deleted"}


