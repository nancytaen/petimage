import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URI = os.environ.get("DATABASE_URI")

    SMTP_MAIL_ADDR = os.environ.get("SMTP_MAIL_ADDR")
    SMTP_MAIL_PWD = os.environ.get("SMTP_MAIL_PWD")
