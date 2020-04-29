from flask import Blueprint, jsonify
import json

from taskobra.orm import *

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/')
def base():
    return jsonify({})

@blueprint.route('/systems')
def hostnames():
    systems = [
                                  # Switch Status/Uptime/Misc -> Num Cores / Memory Size / Storage Cap
        {'hostname': system.name,
        'Cores' : sum([component.core_count for _, component in system.components if isinstance(CPU, component)]),
        'uptime': '00:00:00',
        'misc': '' }
        for system in System.query.all()
    ]
    return jsonify(systems)

