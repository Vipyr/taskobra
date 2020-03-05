from contextlib import contextmanager
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


ORMBase = declarative_base()


@lru_cache()
def get_engine(*args, **kwargs):
    return create_engine(*args, **kwargs)


@lru_cache()
def get_sessionmaker(*args, **kwargs):
    return sessionmaker(*args, **kwargs)


@contextmanager
def get_session(*args, **kwargs):
    session = get_sessionmaker(*args, **kwargs)()
    ORMBase.metadata.create_all(session.bind)
    try:
        yield session
        session.commit()
        session.close()
    except:
        session.rollback()
        session.close()
        raise
