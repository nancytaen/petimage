from flask import session
from sqlalchemy import func, and_

from application.model.base import Session
from application.model.posts import Post, Like, Comment
from application.model.users import User
from application.utility.message import PostMessage


def get_my_posts():
    """
    query all posts by session user
    :return: list of dicts of posts
    """
    db_session = Session()
    posts = db_session.query(Post, func.count(Like.like_id)).filter(
        Post.user_id == session['user_id']).outerjoin(Like).group_by(Post.post_id).all()

    my_posts = [{'id': post.post_id, 'title': post.post_title, 'body': post.post_body,
                 'img_url': post.post_img_url, 'like': like,
                 'username': session['username']} for post, like in posts]
    return my_posts


def get_post_detail(post_id):
    db_session = Session()
    post_info = db_session.query(Post, User, func.count(Like.like_id)).filter(Post.post_id == post_id).join(
        User, User.user_id == Post.user_id).outerjoin(
        Like, and_(Like.post_id == post_id, Like.user_id == session['user_id'])).one_or_none()

    if post_info is None:
        return PostMessage.POST_NOT_FOUND

    comments = db_session.query(Comment, func.count(Like.like_id)).filter(Comment.post_id == post_id).join(
        User, User.user_id == Comment.user_id).outerjoin(Like, Like.comment_id == Comment.comment_id).all()

    post = post_info[0]
    user = post_info[1]
    like = post_info[2]

    return {'id': post_id, 'title': post.post_title, 'body': post.post_body, 'img_url': post.post_img_url,
            'comments': [{'comment_body': comment.body, 'like': like} for comment, like in comments] if
            comments[0][0] else [], 'like': True if like else False,
            'user': {'user_id': user.user_id, 'username': user.username}
            }


def create_post_api(post_form):
    """
    add post to db
    :param post_form:
    :return:
    """
    db_session = Session()
    new_post = Post(session['user_id'])
    post_form.populate_obj(new_post)
    db_session.add(new_post)
    db_session.commit()
    return True
