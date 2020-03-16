from contextlib import contextmanager
from functools import lru_cache
import inspect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import _declarative_constructor
from sqlalchemy.orm import sessionmaker


def __init__ORMBase(self, *args, **kwargs):
    _declarative_constructor(self, *args, **kwargs)
    for name, member in inspect.getmembers(type(self)):
        if name not in kwargs and hasattr(member, "default") and member.default:
            setattr(self, name, member.default.arg)

ORMBase = declarative_base(constructor=__init__ORMBase)


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
