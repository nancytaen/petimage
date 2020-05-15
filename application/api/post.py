from flask import session
from sqlalchemy import func, desc, and_, distinct

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

    posts = db_session.query(Post, func.count(distinct(Like.like_id))).filter(
        and_(Post.user_id == session['user_id'], Post.is_deleted == False)).outerjoin(
        Like, and_(Like.user_id == session['user_id'], Like.is_unliked == False,
                   Like.post_id == Post.post_id)).group_by(Post.post_id).order_by(
        desc(Post.updated_at)).all()
    likes = db_session.query(Like.post_id, func.count(distinct(Like.like_id))).filter(
        Like.is_unliked == False).join(Post, Post.user_id == session['user_id']).group_by(Like.post_id).all()
    comments = db_session.query(Comment.post_id, func.count(distinct(Comment.comment_id))).filter(
        Comment.is_deleted == False).join(Post, Post.user_id == session['user_id']).group_by(Comment.post_id).all()

    my_posts = [{'id': post.post_id, 'title': post.post_title, 'body': post.post_body,
                 'img_url': post.post_img_url, 'liked': True if like else False,
                 'username': session['username']} for post, like in posts]
    for like in likes:
        my_posts[len(my_posts) - like[0]]['likes'] = like[1]
    for comment in comments:
        my_posts[len(my_posts) - comment[0]]['comments'] = comment[1]

    return my_posts


def get_post_detail(post_id):
    """
    query post details including likes and comments
    :param post_id:
    :return:
    """
    db_session = Session()
    post_info = db_session.query(Post, User, func.count(distinct(Like.like_id))).filter(Post.post_id == post_id).join(
        User, User.user_id == Post.user_id).outerjoin(
        Like, and_(Like.post_id == post_id, Like.user_id == session['user_id'], Like.is_unliked == False)).one_or_none()

    if post_info is None:
        return PostMessage.POST_NOT_FOUND

    comments = db_session.query(Comment, User.username).filter(Comment.post_id == post_id).join(
        User, User.user_id == Comment.user_id).all()
    likes = db_session.query(User.username).join(Like, Like.user_id == User.user_id).filter(and_(
        Like.post_id == post_id, Like.is_unliked == False)).all()

    post = post_info[0]
    user = post_info[1]
    like = post_info[2]

    return {'id': post.post_id, 'title': post.post_title, 'body': post.post_body, 'img_url': post.post_img_url,
            'liked': True if like else False, 'likes': likes,
            'comments': [{'comment_body': comment.body, 'username': username} for comment, username in comments],
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


def like_post_api(post_id):
    """
    like post
    :param post_id:
    :return: False if error occurs
    """

    db_session = Session()
    try:
        existing_like = db_session.query(Like).filter(and_(Like.post_id == post_id, Like.user_id == session['user_id'])).one_or_none()
        if existing_like:
            existing_like.is_unliked = not existing_like.is_unliked
        else:
            db_session.add(Like(post_id, session['user_id']))
        db_session.commit()
        db_session.close()
    except Exception as e:
        print(e)
        return False
    return True
