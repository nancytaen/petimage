from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from application.model.base import Base
from config import configObject


try:
    engine = create_engine(configObject.DATABASE_URI, convert_unicode=True, echo=True)
    db_session = scoped_session(sessionmaker(autocomit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()

except Exception as e:
    print("Database Connection Error")
    print(e)


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as ex:
        print(ex)
