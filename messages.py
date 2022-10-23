from db import db
import users

def get_messages_list():
    sql = 'select m.id, m.headline, m.content, m.sent_at, m.user_id, u.username from messages m, users u where m.user_id=u.id order by m.id desc'
    result = db.session.execute(sql)
    return result.fetchall()

def get_message(id):
    sql = 'select m.id, m.headline, m.content, m.sent_at, m.user_id, u.username from messages m, users u where m.id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchone()

def send(headline, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (headline, content, user_id, sent_at) VALUES (:headline, :content, :user_id, NOW())"
    db.session.execute(sql, {"headline":headline,"content":content, "user_id":user_id})
    db.session.commit()
    return True


def delete_message(message_id, user_id):
    sql = 'UPDATE messages SET deleted = True WHERE id = :message_id AND user_id = :user_id'
    db.session.execute(sql, {'message_id': message_id, 'user_id': user_id})
    db.session.commit()