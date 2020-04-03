from flask import Blueprint, jsonify


blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/')
def base():
    """
    Base API Route, not sure what this should return
    Probably TODO remove, and replace with interesting routes 
    """
    return jsonify({})
    