from db import db
import users

def liked(id):
    message_id = id
    user_id = users.user_id()
    sql = 'SELECT liked FROM likes WHERE user_id=:user_id AND message_id=:message_id'
    result = db.session.execute(sql, {'user_id':user_id, 'message_id':message_id}).fetchone()
    if result is not None:
        result = result[0]
    if result == 0:
        sql = 'UPDATE likes SET liked=1 WHERE user_id=:user_id AND message_id=:message_id'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    elif result == 1:
        sql = 'UPDATE likes SET liked=0 WHERE user_id=:user_id AND message_id=:message_id'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    else:
        sql = 'INSERT INTO likes (liked, user_id, message_id, disliked) VALUES (1, :user_id, :message_id, 0)'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    return result

def get_likes(message_id):
    sql = 'SELECT sum(liked) FROM likes WHERE message_id=:message_id'
    return db.session.execute(sql, {'message_id':message_id}).fetchone()[0]


def disliked(id):
    message_id = id
    user_id = users.user_id()
    sql = 'SELECT disliked FROM likes WHERE user_id=:user_id AND message_id=:message_id'
    result = db.session.execute(sql, {'user_id':user_id, 'message_id':message_id}).fetchone()
    if result is not None:
        result = result[0]
    if result == 0:
        sql = 'UPDATE likes SET disliked=1 WHERE user_id=:user_id AND message_id=:message_id'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    elif result == 1:
        sql = 'UPDATE likes SET disliked=0 WHERE user_id=:user_id AND message_id=:message_id'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    else:
        sql = 'INSERT INTO likes (liked, user_id, message_id, disliked) VALUES (0, :user_id, :message_id, 1)'
        db.session.execute(sql, {'user_id':user_id, 'message_id':message_id})
        db.session.commit()
    return result

def get_dislikes(message_id):
    sql = 'SELECT sum(disliked) FROM likes WHERE message_id=:message_id'
    return db.session.execute(sql, {'message_id':message_id}).fetchone()[0]