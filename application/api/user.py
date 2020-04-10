from application.model.base import db_session
from application.model.user_model import User

from application.message import UserMessage


def signup_api(signup_form):
    session = db_session()
    # check if email is used
    if find_existing_user(signup_form.email.data, session) is not False:
        return signup_form.email.data + UserMessage.USER_EXISTS

    # insert into db
    session.add(User(signup_form.email.data, signup_form.password.data))
    session.commit()
    session.close()

    return UserMessage.SIGNUP_SUCCESS


def login_api(login_form):
    session = db_session()
    matched_user = find_existing_user(login_form.email.data, session)
    if matched_user is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    if matched_user.authenticate_password(login_form.password.data) is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    return UserMessage.LOGIN_SUCCESS


def find_existing_user(email, session):
    existing_user = session.query(User).filter(User.email == email).first()
    if existing_user is None:
        return False
    return existing_user

