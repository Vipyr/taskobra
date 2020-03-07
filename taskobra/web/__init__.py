
from flask import Flask
import os

def create_app(config=None):
    """
    Taskobra Web Application Factory
        Constructs Flask WSGI Application 
    return -- Flask()
    """
    app = Flask(__name__, 
            template_folder='static/html',  # Root path for render_template() 
            static_folder='static')         # Root Path for url_for('static')

    # Bind Route Blueprints Packages to the base App
    from .views import api, ui
    app.register_blueprint(api.blueprint)
    app.register_blueprint(ui.blueprint)

    return app

