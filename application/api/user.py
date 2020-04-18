from flask import session

from application.model.base import Session
from application.model.users import User
from application.message import UserMessage


def signup_api(signup_form):
    db_session = Session()
    if find_existing_user(signup_form.email.data, db_session) is not False:
        # if email is used, return error
        return signup_form.email.data + UserMessage.USER_EXISTS

    # insert into db
    new_user = User(signup_form.email.data, signup_form.password.data)
    new_user.set_unique_username(db_session)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

    return UserMessage.SIGNUP_SUCCESS


def login_api(login_form):
    db_session = Session()
    matched_user = find_existing_user(login_form.email.data, db_session)
    if matched_user is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    if matched_user.authenticate_password(login_form.password.data) is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    session['logged_in'] = True
    session['user_id'] = matched_user.user_id
    session['username'] = matched_user.username
    return UserMessage.LOGIN_SUCCESS


def find_existing_user(email, db_session):
    existing_user = db_session.query(User).filter(User.email == email).first()
    if existing_user is None:
        return False
    return existing_user

