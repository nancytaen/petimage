from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from application.model.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
