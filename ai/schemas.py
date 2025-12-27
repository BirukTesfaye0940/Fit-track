from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID

class ParsedExercise(BaseModel):
  name: str
  muscle_group: Optional[str]
  equipment: Optional[str]
  sets: int
  reps: int
  weight: int
  rpe: Optional[int]
  confidence: float

class ParsedWorkout(BaseModel):
  date: Optional[date]
  notes: Optional[str]
  exercises: List[ParsedExercise]
  
class AIWorkoutLogRequest(BaseModel):
  text: str

class AICreatedExercise(BaseModel):
  name: str
  confidence: float

class AIWorkoutLogResponse(BaseModel):
  workout_id: UUID
  status: str
  ai_created_exercises: List[AICreatedExercise]