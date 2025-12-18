import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.base_class import Base

class Exercise(Base):
  __tablename__ = "exercises"

  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  muscle_group: Mapped[str] = mapped_column(String(50))
  equipment: Mapped[str] = mapped_column(String(50))

  image_path: Mapped[str | None] = mapped_column(String, nullable=True)