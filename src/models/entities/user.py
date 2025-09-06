# pylint: disable=not-callable
import enum
from uuid import uuid4
from sqlalchemy import UUID, Column, DateTime, Enum, String, Integer
from sqlalchemy.sql import func
from src.db.base import Base

class UserRoleEnum(str, enum.Enum):
    PLAYER = "player"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(length=120), nullable=False)
    username = Column(String(length=50), nullable=False, unique=True)
    email = Column(String(length=120), nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.PLAYER, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    rating = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"<User id='{self.id}' username='{self.username}' level='{self.level}'>"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "level": self.level,
            "rating": self.rating,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
