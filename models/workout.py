from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from db.base import Base

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    mood: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(String(255))

    sets = relationship("WorkoutSet", back_populates="workout", cascade="all, delete")
