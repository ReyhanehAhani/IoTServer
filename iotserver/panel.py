from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from iotserver.auth import login_required
from iotserver.db import get_db

bp = Blueprint('panel', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/login')
def login():
    return render_template('auth/base.html', authForm=url_for('auth.login'), authType='Logged in', authTarget=url_for('panel.dashboard'), pageType='Login', pageButton='Login')


@bp.route('/register')
def register():
    return render_template('auth/base.html', authForm=url_for('auth.register'), authType='Registered', authTarget=url_for('panel.index'), pageType='Register', pageButton='Register')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard/summary.html')


@bp.route('/settings')
@login_required
def settings():
    return render_template('dashboard/settings.html')


@bp.route('/devices')
@login_required
def devices():
    db = get_db()
    records = db.execute(
        "SELECT id, username FROM `user` ORDER BY id ASC").fetchall()
    return render_template('dashboard/devices.html', records=records)

@bp.route('/records')
@login_required
def records():
    return render_template('dashboard/records.html')
