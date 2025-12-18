from pydantic import BaseModel
from datetime import date
from uuid import UUID

class WorkoutCreate(BaseModel):
  date: date
  duration_minutes: int
  mood: str | None = None
  notes: str | None = None

class WorkoutRead(WorkoutCreate):
  id: UUID

  class Config:
    from_attributes = True