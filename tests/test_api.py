import sqlite3

import pytest
from flask import g, session
from iotserver.db import get_db


def test_records(app, client):
    with client:
        r = client.post(
            '/auth/login', data={'password': 'test', 'username': 'test'})
        assert r.status_code == 200
        assert r.get_json() == {"result": "success"}
        assert g.user['username'] == 'test'
        assert session['user_id'] == 1

        r = client.get('/api/fetch_recent_record')
        assert r.get_json()['result'] == 'success'


def test_insert(app, client):
    with client:
        r = client.post(
            '/auth/login', data={'password': 'test', 'username': 'test'})
        assert r.status_code == 200
        assert r.get_json() == {"result": "success"}
        assert g.user['username'] == 'test'
        assert session['user_id'] == 1

        r = client.get('/api/insert_record', data={'id': '1', 'ir': '100',
                                                   'light': '100', 'moisture': '100', 'temperature': '10'})

        assert r.status_code == 200
        assert r.get_json() == {"result": "success"}

        r = client.get('/api/insert_record', data={'id': '1', 'ir': '100',
                                                   'light': '100', 'temperature': '10'})

        assert r.status_code == 400
        assert r.get_json() == {
            "result": "failure",
            "reason": "Incomplete record data"
        }
