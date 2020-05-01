import re
import enum
import secrets
import hashlib
from datetime import datetime

from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from application.model.base import Base


class UserStatus(enum.Enum):
    temporary = 0
    active = 1
    deleted = 2


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    email = Column(String(30), nullable=False, unique=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    profile_img_url = Column(String(128))
    name_idx = Column(SmallInteger, nullable=False, default=0)
    user_status = Column(Enum(UserStatus), default=UserStatus.temporary)

    token = relationship("Token", backref="user")
    post = relationship("Post", backref="user")
    like = relationship("Like", backref="user")
    comment = relationship("Comment", backref="user")
    tag = relationship("Tag", backref="user")

    # for creating User instance
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    # check password
    def authenticate_password(self, check_password):
        if check_password_hash(self.password, check_password):
            return True
        else:
            return False

    def set_unique_username(self, db_session):
        self.username = re.split('[.@]', self.email)[0]
        existing_username = db_session.query(User).filter(User.username == self.username).one_or_none()
        if existing_username:
            self.username += str(existing_username.name_idx)
            existing_username.name_idx = existing_username.name_idx + 1
        return self.username

    def generate_verif_token(self, token_type):
        raw_token = hashlib.sha256((token_type + secrets.token_urlsafe(20)
                                    + self.username + self.email + str(datetime.now())).encode()).hexdigest()
        return raw_token
