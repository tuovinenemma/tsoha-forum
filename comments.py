from db import db
import users

def get_comments_list(id):
    message_id = id
    sql = 'select c.id, c.content, c.sent_at, c.user_id, u.username from comments c, users u where c.message_id=:message_id and c.user_id=u.id order by c.id desc'
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchall()

def get_comment(id):
    sql = 'select c.id, c.content, c.sent_at, c.user_id, u.username from comments c, users u where c.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def send_comment(content, message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (content, message_id, user_id,  sent_at) VALUES (:content, :message_id, :user_id,  NOW())"
    db.session.execute(sql, {"content":content, "message_id":message_id, "user_id":user_id})
    db.session.commit()
    return True