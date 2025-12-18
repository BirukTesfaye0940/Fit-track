from pydantic import BaseModel
from uuid import UUID

class WorkoutSetCreate(BaseModel):
  exercise_id: UUID
  reps: int
  weight: int
  rpe: int | None = None

class WorkoutSetRead(WorkoutSetCreate):
  id: UUID
  workout_id: UUID

  class Config:
    from_attributes = True