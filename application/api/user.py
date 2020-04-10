from application.model.base import db_session
from application.model.user_model import User

from application.message import UserMessage


def api_signup(signup_form):
    session = db_session()
    print(signup_form)
    # check if email is used
    if find_existing_user(signup_form.email.data, session) is not False:
        return signup_form.email.data + UserMessage.USER_EXISTS

    # insert into db
    session.add(User(signup_form.email.data, signup_form.password.data))
    session.commit()
    session.close()

    return UserMessage.SIGNUP_SUCCESS


def find_existing_user(email, session):
    existing_user = session.query(User).filter(User.email == email).first()
    if existing_user is None:
        return False
    return User

