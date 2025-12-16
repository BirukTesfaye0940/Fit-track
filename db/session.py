from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from typing import Generator

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/fittrack"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
  autocommit=False, 
  autoflush=False, 
  bind=engine
)

def get_db() -> Generator[Session, None, None]:
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()