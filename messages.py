from db import db
import users

def get_list():
    sql = "SELECT M.headline, M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(headline, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (id, headline, content, user_id, sent_at) VALUES (:headline, :content, :user_id, NOW())"
    db.session.execute(sql, {"id":id, "headline":headline,"content":content, "user_id":user_id})
    db.session.commit()
    return True

def get_message_info(id):
    sql = "SELECT M.headline, U.name FROM messages M, users U WHERE M.id=:id AND M.user_id=u.id"
    return db.session.execute(sql, {"id":id}).fetchone()

def show_message(id, headline, content):
    sql = 'SELECT M.id M.headline, M.content, M.user_id U.username FROM messages M, users U WHERE M.id=:id ORDER by id desc'
    return db.session.execute(sql, {'id':id}).fetchall()