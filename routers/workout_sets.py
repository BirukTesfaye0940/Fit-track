from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.ownership import get_owned_workout


from db.session import get_db
from models.workout_set import WorkoutSet
from schemas.workout_set import WorkoutSetCreate, WorkoutSetRead
from routers.auth import get_current_user

router = APIRouter(prefix="/workout-sets", tags=["Workout Sets"])

@router.post("/workouts/{workout_id}/sets", response_model=WorkoutSetRead)
def add_set(
    workout_id: int,
    workout_set: WorkoutSetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    get_owned_workout(workout_id, current_user["id"], db)

    db_set = WorkoutSet(workout_id=workout_id, **workout_set.dict())
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

