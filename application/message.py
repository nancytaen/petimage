# user related messages
class UserMessage:
    SIGNUP_SUCCESS = "Account has been successfully created."
    LOGIN_SUCCESS = 0
    USER_EXISTS = " is already used."
    EMAIL_PASSWORD_NOT_MATCH = " Email or password is wrong."
    EMAIL_ERROR = "Something went wrong. Please try again later"


class TokenMessage:
    VERIFY_SUCCESS = 0
    TOKEN_NOT_FOUND = "The url has expired. Please register again."
    TOKEN_EXPIRED = "The link has expired. "
    TOKEN_INCORRECT = "The token is incorrect."