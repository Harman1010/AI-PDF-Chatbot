from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base

class User(Base):

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)

    email:  Mapped[str] = mapped_column(String, unique=True, nullable= False, index=True)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

