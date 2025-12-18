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

