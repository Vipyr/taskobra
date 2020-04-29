
import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from taskobra.orm import *
from taskobra.web.views import api, ui


# Set Up Database Bindings
engine = create_engine(os.environ.get('DATABASE_URI', 'sqlite:///taskobra.sqlite.db'))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
ORMBase.query = db_session.query_property()

def init_db():
    import taskobra.orm
    ORMBase.metadata.create_all(bind=engine)
