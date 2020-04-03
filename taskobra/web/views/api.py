from flask import Blueprint, jsonify
import json

from taskobra.orm import *

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/')
def base():
    """
    Base API Route, not sure what this should return
    Probably TODO remove, and replace with interesting routes 
    """
    return jsonify({})
    
@blueprint.route('/hostnames')
def hostnames():
    """
    Base API Route, not sure what this should return
    Probably TODO remove, and replace with interesting routes 
    """
    hostnames = [system.name for system in System.query.all()]
    return json.dumps(hostnames)
    
