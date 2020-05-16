from datetime import datetime, timedelta

from flask import session
from sqlalchemy import and_, func, distinct

from application.model.base import Session
from application.model.users import User, UserStatus, Follow
from application.model.tokens import Token, TokenType, TokenStatus
from application.utility.message import UserMessage, TokenMessage
from application.send_mail import send_mail
from config import Config


def get_current_user_obj(db_session):
    return db_session.query(User).filter(User.user_id == session['user_id']).one()


def get_follow_info_by_username(db_session, username):
    """
    obtain user_id of user with username
    :param db_session:
    :param username:
    :return: return dict of user_id, follows #, followers #/ None if username not found
    """

    following = db_session.query(User.user_id, func.count(distinct(Follow.follow_id))).filter(and_(
        User.username == username, User.user_status == UserStatus.active)).outerjoin(
        Follow, Follow.user_id == User.user_id).one_or_none()
    followers = db_session.query(func.count(distinct(Follow.follow_id))).join(User, and_(
        User.username == username, User.user_status == UserStatus.active)).filter(
        Follow.follow_user_id == User.user_id).scalar()
    return {'user_id': following[0], "follows": following[1], "followers": followers} if following[0] else None


def signup_api(signup_form):
    """
    api that registers new users
    :param signup_form: WTForm filled form
    :return: an appropriate success or failure message from message.py
    """
    db_session = Session()
    if db_session.query(User).filter(User.email == signup_form.email.data,
                                     User.user_status != UserStatus.deleted).one_or_none() is not None:
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
    matched_user = db_session.query(User).filter(User.email == login_form.email.data,
                                                 User.user_status == UserStatus.active).one_or_none()
    if matched_user is None:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    if matched_user.authenticate_password(login_form.password.data) is False:
        return UserMessage.EMAIL_PASSWORD_NOT_MATCH
    session['logged_in'] = True
    session['user_id'] = matched_user.user_id
    session['username'] = matched_user.username
    session['profile_img'] = matched_user.profile_img_url
    return UserMessage.LOGIN_SUCCESS


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
    """
    verify a token and updates appropriate table
    :param email: email of user
    :param token: token
    :return: appropriate success/fail message of class TokenMessage
    """
    db_session = Session()
    db_obj = db_session.query(User, Token).filter(
        User.email == email, User.user_status == UserStatus.temporary).filter(
        Token.user_id == User.user_id, Token.token_status == TokenStatus.pending,
        Token.token_type == TokenType.email_verify).one_or_none()
    if db_obj is None:
        return TokenMessage.TOKEN_NOT_FOUND

    user_obj = db_obj[0]
    token_obj = db_obj[1]

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
