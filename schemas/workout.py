from pydantic import BaseModel
from datetime import date

class WorkoutCreate(BaseModel):
  date: date
  duration_minutes: int
  mood: str | None = None
  notes: str | None = None

class WorkoutRead(WorkoutCreate):
  id: int

  class Config:
    from_attributes = True