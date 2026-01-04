from typing import Optional
from pydantic import BaseModel
from uuid import UUID

from schemas.exercise import ExerciseRead

class WorkoutSetCreate(BaseModel):
  exercise_id: UUID
  reps: int
  weight: int
  rpe: Optional[int] = None

class WorkoutSetRead(WorkoutSetCreate):
  id: UUID
  workout_id: UUID
  exercise: Optional[ExerciseRead] = None

  class Config:
    from_attributes = True

class WorkoutSetUpdate(BaseModel):
  reps: Optional[int] = None
  weight: Optional[int] = None
  rpe: Optional[int] = None