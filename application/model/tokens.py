import enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func

from application.model.base import Base


class TokenType(enum.Enum):
    email_verify = 0
    password_forgot = 1


class Token(Base):
    __tablename__ = 'token'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    token_body = Column(String(128), nullable=False)
    token_type = Column(Enum(TokenType))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __init__(self, token):
        self.token_body = token
