import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from taskobra.orm import *
from taskobra.web.views import api, ui


def create_app():
    """
    Taskobra Web Application Factory
        Constructs Flask WSGI Application
    return -- Flask()
    """
    app = Flask(__name__,
            template_folder='static/html',  # Root path for render_template()
            static_folder='static')         # Root Path for url_for('static')

    # Load config from ENV
    app.config['DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///taskobra.sqlite.db')
    # TODO: OAuth Key
    # TODO: ???
    print(f" * Using Database URI {app.config['DATABASE_URI']}")
    # Bind Route Blueprints Packages to the base App
    app.register_blueprint(api.blueprint)
    app.register_blueprint(ui.blueprint)

    # Set Up Database Bindings
    engine = create_engine(app.config['DATABASE_URI'])
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    ORMBase.query = db_session.query_property()
    ORMBase.metadata.create_all(bind=engine)

    return app

