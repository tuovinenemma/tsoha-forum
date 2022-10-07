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
            session['user_id'] = user[0]
            session['username'] = user[1]
            return True
        return False

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = 'insert into users (username, password) values (:username, :password)'
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

