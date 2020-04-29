from flask import Blueprint, jsonify
import json
import random
import statistics

from taskobra.orm import *
from taskobra.web import db

blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/')
def base():
    return jsonify({})

@blueprint.route('/systems')
def systems():
    system_list = [
        {'hostname': system.name,
        'cores' : sum([component.core_count for _, component in system.components if isinstance(component, CPU)]),
        'memory': '16GB', 'storage': '500GB' }
        for system in System.query.all()
    ]
    return jsonify(system_list)

@blueprint.route('/metrics/cpu')
def metrics_cpu():
    # [ [x, y], [x2, y2] ... ]
    #CPUPercent.join(Systems).query(system.system_name == "")
    percent_list = []
    snapshots = Snapshot.query.all()
    for snapshot in snapshots:
        cpu_percent = []
        for metric in snapshot.metrics:
            if isinstance(metric, CpuPercent):
                cpu_percent.append(metric.mean)
        #total_cpu = statistics.mean(
        #    metric.mean for metric in snapshot.metrics if isinstance(metric, CpuPercent)
        #)
        total_cpu = statistics.mean(cpu_percent)
        percent_list.append([snapshot.timestamp, total_cpu])

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

@blueprint.route('/prune')
def prune():
    for old, new in Snapshot.prune(db.session.query(Snapshot)):
        if old:
            db.session.delete(old)
        if new:
            db.session.add(new)
        db.session.commit()
    return jsonify({})
