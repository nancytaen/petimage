import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URI = os.environ.get("DATABASE_URI")

    SMTP_MAIL_ADDR = os.environ.get("SMTP_MAIL_ADDR")
    SMTP_MAIL_PWD = os.environ.get("SMTP_MAIL_PWD")
    ROOT_URL = os.environ.get("ROOT_URL")

    S3_BUCKET = os.environ.get("S3_BUCKET")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
