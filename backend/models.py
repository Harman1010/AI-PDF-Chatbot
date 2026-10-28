from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime

from datetime import datetime

from backend.database import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id: Mapped[str | None] = mapped_column(String,nullable=True)
    session_id: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    filename: Mapped[str] = mapped_column(String,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now,nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)