import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from iotserver.db import get_db

import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

# decorator for pages that require loggin in


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('/')

        return view(**kwargs)

    return wrapped_view

USERNAME_REGEX = re.compile('^[a-zA-Z0-9]+$')
PASSWORD_REGEX = re.compile('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$')

@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method != "POST":
        return {
            "result": "failure",
            "reason": "Invalid method"
        }, 405

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    db = get_db()

    if not username or not password:
        return {
            "result": "failure",
            "reason": "Invalid password or username"
        }, 401

    if not USERNAME_REGEX.match(username) or not PASSWORD_REGEX.match(password):
        return {
            "result": "failure",
            "reason": "Invalid password or username"
        }, 401

    try:
        db.execute("INSERT INTO `user` (`username`, `password`) VALUES (?, ?)",
                   (username, generate_password_hash(password)), )
        db.commit()
        return {"result": "success"}, 200
    except db.IntegrityError:
        return {
            "result": "failure",
            "reason": "User already exists"
        }, 401


@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method != "POST":
        return {
            "result": "failure",
            "reason": "Invalid method"
        }, 405

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    db = get_db()

    if not username or not password:
        return {
            "result": "failure",
            "reason": "Invalid password or username"
        }, 401

    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (
            username,)
    ).fetchone()

    if user is None:
        return {
            "result": "failure",
            "reason": "Incorrect username",
        }, 401

    if not check_password_hash(user['password'], password):
        return {
            "result": "failure",
            "reason": "Incorrect password",
        }, 401

    session.clear()
    session['user_id'] = user['id']
    g.user = user

    return {"result": "success"}, 200


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')


@bp.route('/change_username', methods=["POST", "GET"])
@login_required
def change_username():
    if request.method != "POST":
        return {
            "result": "failure",
            "reason": "Invalid method"
        }, 405

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    db = get_db()

    if not username or not password:
        return {
            "result": "failure",
            "reason": "Invalid password or username"
        }, 401

    if not check_password_hash(g.user['password'], password):
        return {
            "result": "failure",
            "reason": "Incorrect passwors"
        }, 401

    db.execute('UPDATE OR REPLACE `user` SET `username` = ? WHERE `id` = ?;',
               (username, g.user['id']))
    db.commit()

    return {"result": "success"}, 200


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
