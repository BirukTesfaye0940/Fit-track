from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  username: Optional[str] = None
  email: Optional[EmailStr] = None
  password: str

class UserRead(BaseModel):
  id: int
  username: str
  email: EmailStr
  
  class Config:
    from_attributes = True

class Token(BaseModel):
  access_token: str
  token_type: str