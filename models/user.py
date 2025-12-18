import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from db.base_class import Base

class User(Base):
  __tablename__ = "users"
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
  

  