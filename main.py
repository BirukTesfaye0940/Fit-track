from fastapi import FastAPI
from routers.exercises import router as exercises_router
from routers.auth import router as auth_router

from db.session import engine
from db.base import Base
from models.exercise import Exercise
from models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(exercises_router)
app.include_router(auth_router)

@app.get("/")
async def root():
  return {"message": "FitTrack API is alive"}