from flask import Blueprint, jsonify
import json
import random

from taskobra.orm import *

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/')
def base():
    return jsonify({})
    
@blueprint.route('/systems')
def systems():
    system_list = [
        {'hostname': system.name, 'status' : 'Good', 'uptime': '00:00:00', 'misc': '' }
        for system in System.query.all()
    ]
    return jsonify(system_list)
    
@blueprint.route('/metrics/cpu')
def metrics_cpu():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)

@blueprint.route('/metrics/gpu')
def metrics_gpu():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)

@blueprint.route('/metrics/memory')
def metrics_memory():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)

@blueprint.route('/metrics/storage')
def metrics_storage():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)
