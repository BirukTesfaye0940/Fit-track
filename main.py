from fastapi import FastAPI
from routers.exercises import router as exercises_router

from db.session import engine
from db.base import Base
from models.exercise import Exercise

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(exercises_router)

@app.get("/")
async def root():
  return {"message": "FitTrack API is alive"}