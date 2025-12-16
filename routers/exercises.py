from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.exercise import ExerciseCreate, ExerciseRead
from models.exercise import Exercise

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.post("/", response_model=ExerciseRead)
def create_exercise(
  exercise: ExerciseCreate,
  db: Session = Depends(get_db)
):
  db_exercise = Exercise(**exercise.dict())
  db.add(db_exercise)
  db.commit()
  db.refresh(db_exercise)
  return db_exercise

@router.get("/", response_model=list[ExerciseRead])
def list_exercises(db: Session = Depends(get_db)):
  return db.query(Exercise).all()