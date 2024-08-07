from fastapi import FastAPI,APIRouter
from core.config import settings
from database import engine,Base
from routers import user,cinemas,hall,movie,showing,seat,book,auth



# def create_table():
#     Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title= settings.project_name,version = settings.project_version)
    create_table()
    return app

app = start_application()

app.include_router(user.router)
app.include_router(cinemas.router)
app.include_router(hall.router)
app.include_router(movie.router)
app.include_router(showing.router)
app.include_router(seat.router)
app.include_router(book.router)
app.include_router(auth.router)
