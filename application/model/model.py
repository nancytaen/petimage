from sqlalchemy import create_engine

from application.model.base import Session, Base
from config import Config


def init_db():
    try:
        engine = create_engine(Config.DATABASE_URI, convert_unicode=True, echo=False)
        Session.configure(bind=engine)
        Base.query = Session.query_property()

    except Exception as e:
        print("Database Connection Error")
        print(e)
