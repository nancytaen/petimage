import enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

from application.model.base import Base


class TokenType(enum.Enum):
    email_verify = 0
    password_forgot = 1


class TokenStatus(enum.Enum):
    pending = 0
    verified = 1
    inactive = 2


class Token(Base):
    __tablename__ = 'token'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    token_body = Column(String(128), nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    token_type = Column(Enum(TokenType), nullable=False)
    token_status = Column(Enum(TokenStatus), default=TokenStatus.pending)

    def __init__(self, token, token_type, user_id):
        self.token_body = generate_password_hash(token)
        self.token_type = token_type
        self.user_id = user_id

    def verify_token(self, check_token):
        if check_password_hash(self.token_body, check_token):
            return True
        else:
            return False
