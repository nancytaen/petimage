from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from application.model.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    # for creating User instance
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    # check password
    def authenticate_password(self, password):
        hashed = generate_password_hash(password)
        if check_password_hash(hashed, self.password):
            return True
        else:
            return False
