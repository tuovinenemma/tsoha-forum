from db import db
import users

def get_review_list():
    sql = "SELECT R.content, U.username, R.sent_at FROM reviews R, users U WHERE R.user_id=U.id ORDER BY R.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send_review(content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO reviews (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "user_id":user_id})
    db.session.commit()
    return True