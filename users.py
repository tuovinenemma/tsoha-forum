from db import db
from flask import request, session
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
            return True
        return False

def register(username, password):
    hash_value = generate_password_hash(password)
    sql = 'INSERT into users (username, password, role) values (:username, :password)'
    db.session.execute(sql, {'username': username, 'password': hash_value})
    db.session.commit()



