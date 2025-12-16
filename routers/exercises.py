from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM

from db.session import get_db
from schemas.exercise import ExerciseCreate, ExerciseRead
from models.exercise import Exercise

router = APIRouter(prefix="/exercises", tags=["Exercises"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
  
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return {"username": username}
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

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