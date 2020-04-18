from datetime import datetime, timedelta

from flask import session

from application.model.base import Session
from application.model.users import User, UserStatus
from application.model.tokens import Token, TokenType, TokenStatus
from application.message import UserMessage, TokenMessage
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
    # email user
    if send_user_verif_email(new_username, signup_form.email.data, verif_token) == UserMessage.EMAIL_ERROR:
        return UserMessage.EMAIL_ERROR
    db_session.commit()
    db_session.close()

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
    """
    sends an email to newly registered user
    :return: EMAIL_ERROR message if email could not be sent
    """
    subject = "Welcome to Petimage!"
    verif_url = Config.ROOT_URL + "api/email_verif/" + user_email + "/" + verif_token
    text_body = "Dear {},\n\n" \
                "Thank you for joining petimage! \n\n" \
                "To complete your registration, please verify your email by following the link below.\n" \
                "{}\n" \
                "This link expires in 24 hours.\n\n" \
                "You can request another verification within 7 days. \n" \
                "If you did not register for petimage, please disregard this email.\n" \
                "For further inqueries, please contact {}.".format(username, verif_url, Config.SMTP_MAIL_ADDR)
    if send_mail(user_email, subject, text_body) is False:
        return UserMessage.EMAIL_ERROR


def verify_token_url(email, token):
    db_session = Session()
    user_obj, token_obj = db_session.query(User, Token).filter(
        User.email == email, User.user_status == UserStatus.temporary).filter(
        Token.user_id == User.user_id, Token.token_status == TokenStatus.pending).one_or_none()

    # token/user exists?
    if token_obj is None or user_obj is None:
        return TokenMessage.TOKEN_NOT_FOUND
    # token expired?
    if (datetime.now() - timedelta(hours=24)) > token_obj.created_at:
        return TokenMessage.TOKEN_EXPIRED
    # token correct?
    if token_obj.verify_token(token) is False:
        return TokenMessage.TOKEN_INCORRECT

    # update token status and user status
    token_obj.token_status = TokenStatus.verified
    user_obj.user_status = UserStatus.active
    db_session.commit()
    db_session.close()
    return TokenMessage.VERIFY_SUCCESS
