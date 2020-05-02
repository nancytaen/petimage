from flask import session

from application.model.base import Session
from application.model.posts import Post


def create_post_api(post_form):
    db_session = Session()
    new_post = Post(session['user_id'])
    post_form.populate_obj(new_post)
    db_session.add(new_post)
    db_session.commit()
    return True
