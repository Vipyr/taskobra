from flask import Blueprint, render_template, request, redirect, url_for, current_app


blueprint = Blueprint('ui', __name__)

@blueprint.route('/')
def index():
    """
    Base application view, landing page 
    """
    return render_template('home.html')
