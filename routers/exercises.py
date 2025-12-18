from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from uuid import UUID
from sqlalchemy.orm import Session
from routers.auth import get_current_user

from db.session import get_db
from schemas.exercise import ExerciseCreate, ExerciseRead
from models.exercise import Exercise
from pathlib import Path
import shutil

router = APIRouter(prefix="/exercises", tags=["Exercises"])

UPLOAD_DIR = Path("uploads")



@router.post("/", response_model=ExerciseRead)
def create_exercise(
  exercise: ExerciseCreate,
  db: Session = Depends(get_db),
  current_user: dict = Depends(get_current_user)
):
  db_exercise = Exercise(**exercise.dict())
  db.add(db_exercise)
  db.commit()
  db.refresh(db_exercise)
  return db_exercise

@router.get("/", response_model=list[ExerciseRead])
def list_exercises(db: Session = Depends(get_db)):
  return db.query(Exercise).all()

@router.post("/{exercise_id}/image")
def upload_exercise_image(
  exercise_id: UUID,
  file: UploadFile = File(...),
  db: Session = Depends(get_db),
  current_user: dict = Depends(get_current_user)
):
  exercise = db.query(Exercise).filter(Exercise.id == exercise_id, Exercise.user_id == current_user["id"]).first()
  if not exercise:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
  if not file.content_type.startswith("image/"):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
  
  file_path = UPLOAD_DIR / f"exercise_image_{exercise_id}.jpg"

  with file_path.open("wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
  exercise.image_path = str(file_path)
  db.commit()
  return {"image_url": f"/media/exercise_image_{exercise_id}.jpg"}
  