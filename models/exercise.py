from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class Exercise(Base):
  __tablename__ = "exercises"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  muscle_group: Mapped[str] = mapped_column(String(50))
  equipment: Mapped[str] = mapped_column(String(50))