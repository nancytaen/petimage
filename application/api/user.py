from flask import session

from application.model.base import Session
from application.model.users import User
from application.model.tokens import Token, TokenType
from application.message import UserMessage
from application.send_mail import send_mail
from config import Config


def signup_api(signup_form):
    """
    api that registers new users
    :param signup_form: WTForm filled form
    :return: an appropriate success or failure message from message.py
    """
    db_session = Session()
    if find_existing_user(signup_form.email.data, db_session) is not None:
        # if email is used, return error
        return signup_form.email.data + UserMessage.USER_EXISTS

    # insert into db
    new_user = User(signup_form.email.data, signup_form.password.data)
    new_username = new_user.set_unique_username(db_session)
    db_session.add(new_user)
    db_session.flush()
    # email verification token
    verif_token = new_user.generate_verif_token("email_verification")
    new_token = Token(verif_token, TokenType.email_verify, new_user.user_id)
    db_session.add(new_token)
    # db_session.commit()
    db_session.close()

    # email user
    send_user_verif_email(new_username, signup_form.email.data, verif_token)

    return UserMessage.SIGNUP_SUCCESS


def login_api(login_form):
    """
    api that logs a user in. if successful, adds user info to flask session
    :param login_form: WTForm login filled in
    :return: an appropriate success/failure message from message.py
    """
    db_session = Session()
    matched_user = find_existing_user(login_form.email.data, db_session)
    if matched_user is None:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    if matched_user.authenticate_password(login_form.password.data) is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    session['logged_in'] = True
    session['user_id'] = matched_user.user_id
    session['username'] = matched_user.username
    return UserMessage.LOGIN_SUCCESS


def find_existing_user(email, db_session):
    """
    finds an existing user based on email in db
    :param email:
    :param db_session: sqlalchemy session
    :return: user object if a user is found, None otherwise
    """
    existing_user = db_session.query(User).filter(User.email == email).one_or_none()
    return existing_user


def send_user_verif_email(username, user_email, verif_token):
    subject = "Welcome to Petimage!"
    print(verif_token)
    verif_url = "" + verif_token
    text_body = "Dear {},\n\n" \
                "Thank you for joining petimage! \n\n" \
                "To complete your registration, please verify your email by following the link below.\n" \
                "{}\n" \
                "This link expires in 24 hours.\n\n" \
                "If you did not register for petimage, please disregard this email.\n" \
                "For further inqueries, please contact {}.".format(username, verif_url, Config.SMTP_MAIL_ADDR)
    send_mail(user_email, subject, text_body)

