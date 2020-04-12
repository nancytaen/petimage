from sqlalchemy import create_engine

from application.model.base import Session, Base
from config import configObject


def init_db():
    try:
        engine = create_engine(configObject.DATABASE_URI, convert_unicode=True, echo=False)
        Session.configure(bind=engine)
        Base.query = Session.query_property()

    except Exception as e:
        print("Database Connection Error")
        print(e)
