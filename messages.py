from db import db
import users

def get_list():
    sql = "SELECT M.headline, M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_post_subject(id):
    sql = 'SELECT * FROM messages WHERE id=:id'
    return db.session.execute(sql, {'id':id}).fetchone()[0]

def send(headline, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (headline, content, user_id, sent_at) VALUES (:headline, :content, :user_id, NOW())"
    db.session.execute(sql, {"headline":headline,"content":content, "user_id":user_id})
    db.session.commit()
    return True

