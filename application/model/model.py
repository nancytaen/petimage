from sqlalchemy import create_engine

from application.model.base import db_session
from application.model.user_model import *
from config import configObject


try:
    engine = create_engine(configObject.DATABASE_URI, convert_unicode=True, echo=False)
    db_session.configure(bind=engine)
    Base.query = db_session.query_property()

except Exception as e:
    print("Database Connection Error")
    print(e)


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        print(ex)
