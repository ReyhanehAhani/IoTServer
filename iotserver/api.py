from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort

from iotserver.auth import login_required
from iotserver.db import get_db
import json


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route("/fetch_recent_record")
@login_required
def fetch_recent_record():
    db = get_db()
    user = g.user

    limit = request.args.get('limit', 10)
    print(limit)
    

    if limit == 'all':
        records = db.execute(
            "SELECT * FROM `record` WHERE device_id = ?  ORDER BY created DESC", (user['id'], )).fetchall()
    else:
        records = db.execute(
            "SELECT * FROM `record` WHERE device_id = ?  ORDER BY created DESC LIMIT ?", (user['id'], limit, )).fetchall()
    
    response = {
        'result': 'success',
        'data': [dict(record) for record in records]
    }

    return jsonify(response), 200


@bp.route("/insert_record")
@login_required
def insert_record():
    db = get_db()
    user = g.user

    device_id = user['id']
    ir = request.form.get('ir', None)
    light = request.form.get('light', None)
    moisture = request.form.get('moisture', None)
    temperature = request.form.get('temperature', None)

    if not ir or not light or not moisture or not temperature:
        return {
            "result": "failure",
            "reason": "Incomplete record data",
            "ir": ir,
            "moisture": moisture,
            "temperature": temperature,
            "light": light
        }, 400

    db.execute('INSERT INTO `record` (device_id, ir, light, moisture, temperature) VALUES (?, ?, ?, ?, ?)',
               (device_id, ir, light, moisture, temperature))
    db.commit()

    return {"result": "success"}, 200


@bp.route('/get_devices')
@login_required
def get_devices():
    db = get_db()

    limit = request.form.get('limit', 10)

    records = db.execute(
        "SELECT id, username FROM `user` ORDER BY id ASC LIMIT ?", (limit, )).fetchall()

    response = {
        'result': 'success',
        'data': [dict(record) for record in records]
    }

    return jsonify(response), 200
