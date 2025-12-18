import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workout_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("workouts.id"), nullable=False)
    exercise_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exercises.id"), nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    rpe: Mapped[int | None] = mapped_column(Integer)

    workout = relationship("Workout", back_populates="sets")
