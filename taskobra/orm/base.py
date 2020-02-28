from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = None
ORMBase = declarative_base()
Session = sessionmaker()


@wraps(create_engine)
def init_db(*args, **kwargs):
    engine = create_engine(*args, **kwargs)
    Session.configure(bind=engine)
    ORMBase.metadata.create_all(engine)
