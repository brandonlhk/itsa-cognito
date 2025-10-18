from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, Column, DateTime, Enum as SAEnum, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    AGENT = "AGENT"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    full_name = Column(String(255), nullable=True)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.AGENT)
    password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    is_root = Column(Boolean, default=False, nullable=False)


__table_args__ = (
    UniqueConstraint("email", name="uq_users_email"),
)