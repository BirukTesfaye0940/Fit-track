from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from core.pagination import pagination_params
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from services.stats_service import calculate_weekly_volume

from db.session import get_db
from models.workout import Workout
from models.workout_set import WorkoutSet
from schemas.workout import WorkoutCreate, WorkoutRead, WorkoutUpdate
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
      .options(joinedload(Workout.sets).joinedload(WorkoutSet.exercise))
      .filter(Workout.user_id == current_user["id"])
      .offset(params["skip"])
      .limit(params["limit"])
      .all()
    )

@router.get("/{id}", response_model=WorkoutRead)
def get_workout(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    workout = db.query(Workout).options(joinedload(Workout.sets).joinedload(WorkoutSet.exercise)).filter(
        Workout.id == id,
        Workout.user_id == current_user["id"]
    ).first()
    
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return workout

@router.post("/{workout_id}/finalize")
def finalize_workout(
    workout_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    background_tasks.add_task(calculate_weekly_volume, current_user["id"])
    return {"status": "Workout finalized, stats updating"}

@router.patch("/{id}", response_model=WorkoutRead)
def update_workout(
  id: UUID,
  workout_update: WorkoutUpdate,
  db: Session = Depends(get_db),
  current_user: dict = Depends(get_current_user)
):
  workout = db.query(Workout).filter(
    Workout.id == id,
    Workout.user_id == current_user["id"]
  ).first()
  
  if not workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
  
  update_data = workout_update.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(workout, key, value)
    
  db.commit()
  db.refresh(workout)
  return workout

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
  id: UUID,
  db: Session = Depends(get_db),
  current_user: dict = Depends(get_current_user)
):
  workout = db.query(Workout).filter(
    Workout.id == id,
    Workout.user_id == current_user["id"]
  ).first()
  
  if not workout:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
  
  # Cascade delete means related workout sets will be deleted automatically 
  # if configured in the model relationship
  db.delete(workout)
  db.commit()
