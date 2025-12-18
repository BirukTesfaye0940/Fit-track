from pydantic import BaseModel

class WorkoutSetCreate(BaseModel):
  exercise_id: int
  reps: int
  weight: int
  rpe: int | None = None

class WorkoutSetRead(WorkoutSetCreate):
  id: int
  workout_id: int

  class Config:
    from_attributes = True