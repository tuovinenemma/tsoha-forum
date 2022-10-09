from db import db
import os
from flask import request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"    
    result = db.session.execute(sql, {'username': username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user['password']
        if check_password_hash(hash_value, password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['csrf_token'] = os.urandom(16).hex()
            return True
        return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT into users (username, password) values (:username, :password)'
        db.session.execute(sql, {'username': username, 'password': hash_value})
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

def delete_user(username):
    try:
        db.session.execute("DELETE FROM Users WHERE username=:username", {
                                 "username": username})
        db.session.commit()
        return True
    except:
        return False