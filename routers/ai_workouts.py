from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai.gemini_client import parse_workout_text
from mcp.workout_parser import build_workout
from db.session import get_db
from routers.auth import get_current_user

from ai.schemas import AIWorkoutLogRequest, AIWorkoutLogResponse

router = APIRouter(prefix="/ai/workouts", tags=["AI"])

@router.post("/log", response_model=AIWorkoutLogResponse)
def log_workout_nl(
  payload: AIWorkoutLogRequest,
  db: Session = Depends(get_db),
  current_user: dict = Depends(get_current_user)
):
  parsed = parse_workout_text(payload["text"])
  workout, created_exercises = build_workout(
    db=db, 
    user_id=current_user["id"], 
    parsed_workout=parsed
  )
  return {
    "workout_id": workout.id,
    "status": "logged",
    "ai_created_exercises": created_exercises
  }
