import pytest

from flask import g, session
from iotserver.db import get_db


def test_register(client, app):
    r = client.get('/auth/register')
    assert r.status_code == 405
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid method"
    }

    r = client.post('/auth/register')
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid password or username"
    }

    r = client.post('/auth/register', data={'password': '', 'username': ''})
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid password or username"
    }

    r = client.post('/auth/register', data={'password': 'a', 'username': 'a'})
    assert r.status_code == 200
    assert r.get_json() == {"result": "success"}

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

    r = client.post('/auth/register', data={'password': 'a', 'username': 'a'})
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "User already exists"
    }


def test_login(client, app):
    r = client.get('/auth/login')
    assert r.status_code == 405
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid method"
    }

    r = client.post('/auth/login')
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid password or username"
    }

    r = client.post('/auth/login', data={'password': '', 'username': ''})
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Invalid password or username"
    }

    r = client.post(
        '/auth/login', data={'password': 'incorrect', 'username': 'incorrect'})
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Incorrect username",
    }

    r = client.post(
        '/auth/login', data={'password': 'incorrect', 'username': 'test'})
    assert r.status_code == 401
    assert r.get_json() == {
        "result": "failure",
        "reason": "Incorrect password",
    }

    with client:
        r = client.post(
            '/auth/login', data={'password': 'test', 'username': 'test'})
        assert r.status_code == 200
        assert r.get_json() == {"result": "success"}
        assert g.user['username'] == 'test'
        assert session['user_id'] == 1


def test_logout(app, client):
    with client:
        r = client.post(
            '/auth/login', data={'password': 'test', 'username': 'test'})
        assert r.status_code == 200
        assert r.get_json() == {"result": "success"}
        assert g.user['username'] == 'test'
        assert session['user_id'] == 1

        r = client.get('/auth/logout')
        assert 'user_id' not in session
        assert r.location == '/'