import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from db.base_class import Base

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer)
    mood: Mapped[str | None] = mapped_column(String(50))
    notes: Mapped[str | None] = mapped_column(String(255))

    sets = relationship("WorkoutSet", back_populates="workout", cascade="all, delete")
