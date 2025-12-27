from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from routers.exercises import router as exercises_router
from routers.auth import router as auth_router
from routers.workouts import router as workouts_router
from routers.workout_sets import router as workout_sets_router
from routers.stats import router as stats_router
from routers.ai_workouts import router as ai_workouts_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import time

from db.session import engine
from db.base import Base
from models.exercise import Exercise
from models.user import User
from models.workout import Workout
from models.workout_set import WorkoutSet

from core.exceptions import FitTrackException


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(exercises_router)
app.include_router(auth_router)
app.include_router(workouts_router)
app.include_router(workout_sets_router)
app.include_router(stats_router)
app.include_router(ai_workouts_router)

@app.get("/")
async def root():
  return {"message": "FitTrack API is alive"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  return response

@app.exception_handler(FitTrackException)
async def fittrack_exception_handler(request: Request, exc: FitTrackException):
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

MAX_FILE_SIZE = 1024 * 1024 * 5
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    if request.headers.get("content-length"):
        if int(request.headers["content-length"]) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large"
            )
    return await call_next(request)



app.mount(
    "/media",
    StaticFiles(directory="uploads"),
    name="media"
)

origins = [
    "http://localhost:3000",  # dev
    "https://fittrack.app",   # prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)