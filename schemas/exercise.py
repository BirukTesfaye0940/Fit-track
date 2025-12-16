from pydantic import BaseModel

class ExerciseCreate(BaseModel):
  name:str
  muscle_group: str
  equipment: str

class ExerciseRead(ExerciseCreate):
  id: int

  class Config:
    from_attributes = True

