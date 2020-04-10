from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# TODO alembic
Base = declarative_base()
Session = scoped_session(sessionmaker(autoflush=False))
