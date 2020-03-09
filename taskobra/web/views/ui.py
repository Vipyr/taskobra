from flask import Blueprint, render_template

from taskobra.orm import *

blueprint = Blueprint('ui', __name__)

@blueprint.route('/')
def index():
    """
    Base application view, landing page 
    """
    systems = System.query.all()
    return render_template('home.html')
