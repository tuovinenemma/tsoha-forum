from db import db
import os
from flask import request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = 'SELECT id, role, password, username FROM users WHERE username=:username'   
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[2], password):
        session['user_id'] = user[0]
        session['role'] = user[1]
        session['username'] = user[3]
        session['csrf_token'] = os.urandom(16).hex()
        return True


def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username, password, role) VALUES (:username, :password, :role)'
        db.session.execute(
            sql, {'username': username, 'password': hash_value, 'role': role})
        db.session.commit()
    except:
        return False
    return login(username, password)


def user_id():
    return session.get('user_id', 0)

def logout():
    try:
        session.pop('user_id', None)
        session.pop('user_username', None)
    except:
        return False
    return True

def check_csrf():
    if session['csrf_token'] != request.form['csrf_token']:
        abort(403)
