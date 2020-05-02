from flask import session

from application.model.base import Session
from application.model.posts import Post


def get_my_posts():
    """
    query all posts by session user
    :return: list of dicts of posts
    """
    db_session = Session()
    posts = db_session.query(Post).filter(Post.user_id == session['user_id']).all()

    my_posts = [{'id': post.post_id, 'title': post.post_title, 'body': post.post_body,
                 'img_url': post.post_img_url} for post in posts]
    return my_posts


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
