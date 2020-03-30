import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentConfig(Config):
    DATABASE_URI = os.environ.get("DEV_DATABASE_URI")


class ProductionConfig(Config):
    DATABASE_URI = os.environ.get("PROD_DATABASE_URI")


if os.environ.get("FLASK_ENV") == 'production':
    configObject = ProductionConfig
else:
    configObject = DevelopmentConfig
