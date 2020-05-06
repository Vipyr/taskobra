from flask import Blueprint, jsonify, request
import json
import random
import statistics

from taskobra.orm import *
from taskobra.web.database import db_session

blueprint = Blueprint('api', __name__, url_prefix='/api')

def serialize_metrics(host_ids, metric_type):
    percent_list = []
    systems = System.query.filter(System.unique_id.in_(host_ids)).all()
    for idx, system in enumerate(systems):
        for snapshot in system.snapshots:
            total_cpu = statistics.mean(
                metric.mean for metric in snapshot.metrics if isinstance(metric, metric_type)
            )
            snapshot_row = [snapshot.timestamp] + [None] * len(systems)
            snapshot_row[idx+1] = total_cpu
            percent_list.append(snapshot_row)
    return sorted(percent_list, key=lambda row: row[0])

@blueprint.route('/')
def base():
    return jsonify({})

@blueprint.route('/systems')
def systems():
    system_list = [
        {'unique_id' : system.unique_id, 
        'hostname': system.name,
        'cores' : sum([component.core_count for _, component in system.components if isinstance(component, CPU)]),
        'memory': '16GB', 'storage': '500GB' }
        for system in System.query.all()
    ]
    return jsonify(system_list)

@blueprint.route('/metrics/cpu')
def metrics_cpu():
    host_ids = request.args.get('host_ids').split(',')
    percent_list = serialize_metrics(host_ids, CpuPercent)
    return jsonify(percent_list)

@blueprint.route('/metrics/gpu')
def metrics_gpu():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)

@blueprint.route('/metrics/memory')
def metrics_memory():
    host_ids = request.args.get('host_ids').split(',')
    percent_list = serialize_metrics(host_ids, VirtualMemoryUsage)
    return jsonify(percent_list)

@blueprint.route('/metrics/storage')
def metrics_storage():
    percent_list = [
        [idx, random.uniform(0, 100)] for idx in range(0, 1000)
    ]
    return jsonify(percent_list)

@blueprint.route('/prune')
def prune():
    for old, new in Snapshot.prune(db_session.query(Snapshot).order_by(Snapshot.timestamp.desc())):
        if old: db_session.delete(old)
        if new: db_session.add(new)
    db_session.commit()
    return jsonify({})
