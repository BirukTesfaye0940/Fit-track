from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from uuid import UUID
from schemas.workout_set import WorkoutSetRead

class WorkoutCreate(BaseModel):
  date: date
  duration_minutes: Optional[int] = None
  mood: Optional[str] = None
  notes: Optional[str] = None


class WorkoutRead(WorkoutCreate):
  id: UUID
  sets: List[WorkoutSetRead] = []

  class Config:
    from_attributes = True


class WorkoutUpdate(BaseModel):
  date: Optional[date] = None
  duration_minutes: Optional[int] = None
  mood: Optional[str] = None
  notes: Optional[str] = None