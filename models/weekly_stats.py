import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

from db.base_class import Base

class WeeklyStats(Base):
    __tablename__ = "weekly_stats"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)
    total_volume: Mapped[int] = mapped_column(Integer, default=0)
    total_sets: Mapped[int] = mapped_column(Integer, default=0)
    total_reps: Mapped[int] = mapped_column(Integer, default=0)
