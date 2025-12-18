from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from core.pagination import pagination_params
from fastapi import BackgroundTasks
from services.stats_service import calculate_weekly_volume

from db.session import get_db
from models.workout import Workout
from schemas.workout import WorkoutCreate, WorkoutRead
from routers.auth import get_current_user

router = APIRouter(prefix="/workouts", tags=["Workouts"])
    

@router.post("/", response_model=WorkoutRead)
def create_workout(
    workout: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_workout = Workout(user_id=current_user["id"], **workout.dict())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@router.get("/", response_model=list[WorkoutRead])
def list_workouts(
    params = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return (
      db.query(Workout)
      .filter(Workout.user_id == current_user["id"])
      .offset(params["skip"])
      .limit(params["limit"])
      .all()
    )

@router.post("/{workout_id}/finalize")
def finalize_workout(
    workout_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    background_tasks.add_task(calculate_weekly_volume, current_user["id"])
    return {"status": "Workout finalized, stats updating"}
