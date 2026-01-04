from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class ExerciseCreate(BaseModel):
  name:str
  muscle_group: str
  equipment: str

class ExerciseRead(ExerciseCreate):
  id: UUID

  class Config:
    from_attributes = True

class ExerciseUpdate(BaseModel):
  name: Optional[str] = None
  muscle_group: Optional[str] = None
  equipment: Optional[str] = None
