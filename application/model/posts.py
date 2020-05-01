from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship

from application.model.base import Base


class Post(Base):
    """
    table that stores post info
    """
    __tablename__ = 'post'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    post_title = Column(String(20))
    post_body = Column(String(128))
    post_img_url = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    post_tag = relationship("PostTag", backref="post")
    like = relationship('Like', backref='post')
    comment = relationship('Comment', backref='post')


class PostTag(Base):
    """
    table that stores the relationship of post to tags (one to many)
    """
    __tablename__ = 'post_tag'

    tag_id = Column(Integer, ForeignKey('tag.tag_id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    post_tag_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)


class Tag(Base):
    """
    table that stores tags, one to many relationship with User
    """
    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    tag_body = Column(String(20), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)


class Comment(Base):
    """
    table that stores comments
    one to many relationship with Post and User
    """
    __tablename__ = 'comment'

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'), nullable=False)
    comment_body = Column(String(128), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    like = relationship('Like', backref='comment')


class Like(Base):
    """
    table that stores likes to each post or comment
    one-to-many relationship with Post/Comment and User
    """
    __tablename__ = 'like'

    like_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.post_id'))
    comment_id = Column(Integer, ForeignKey('comment.comment_id'))
    is_unliked = Column(Boolean, nullable=False, default=False)
