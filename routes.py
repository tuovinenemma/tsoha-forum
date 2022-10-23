from app import app
from flask import redirect, render_template, request, session, abort
from comments import get_comment, get_comments_list
from db import db
from messages import get_messages_list, get_message, delete_message
import messages, reviews, comments, users
from likes import liked, get_likes, disliked, get_dislikes


@app.route("/")
def index():
    list = get_messages_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route('/message/<int:id>', methods=['get'])
def message(id):
    if request.method == 'GET':
        message = get_message(id)
        list = get_comments_list(id)
        likes = get_likes(id)
        dislikes = get_dislikes(id)
        if likes == None:
            likes = 0
        if dislikes == None:
            dislikes = 0
        return render_template('message.html', id=id, message=message, comments=list, likes=likes, dislikes=dislikes)



@app.route("/message/<int:id>/new_comment", methods=['post'])
def new_comment(id):
    users.check_csrf()
    content = request.form["content"]
    message_id = id
    if comments.send_comment(content, message_id):
        return redirect(f"/message/{message_id}")
    else:
        return render_template("error.html", message="Kommetin lähetys ei onnistunut")


@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    users.check_csrf()
    headline = request.form["headline"]
    content = request.form["content"]

    if len(headline) > 100:
        return render_template("error.html", message="Otsikko on liian pitkä")

    if len(content) > 5000:
        return render_template("error.html", message="Viesti on liian pitkä")

    if not messages.send(headline, content):
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

    else:
        return redirect("/")



@app.route("/new_review")
def new_review():
    list = reviews.get_review_list()
    return render_template("reviews.html", reviews=list)

@app.route("/send_review", methods=["POST"])
def send_review():
    users.check_csrf()
    content = request.form["content"]
    if reviews.send_review(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Palautteen lähetys ei onnistunut")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        users.check_csrf()
        username = request.form['username']

        password = request.form['password']

        if len(username) > 10:
            return render_template('error.html', message='Käyttäjätunnus liian pitkä')
        
        if len(username) < 1:
            return render_template('error.html', message='Käyttäjätunnus liian lyhyt')

        if len(password) > 20:
            return render_template('error.html', message='Salasana liian pitkä')

        if len(password) < 1:
            return render_template('error.html', message='Salasana liian lyhyt')

        role = request.form['role']
        if role not in ['1', '2']:
            return render_template('error.html', message='Rooli vaaditaan kirjautumiseen')

        if users.register(username, password, role):
            return redirect('/')
        else:
            return render_template('error.html', message='Rekisteröinti ei onnistunut')

        

@app.route('/message/<int:id>/like', methods=['get'])
def like(id):
    if request.method == 'GET':
        message_id = id
        liked(message_id)
        return redirect(f'/message/{message_id}')

@app.route('/message/<int:id>/dislike', methods=['get'])
def dislike(id):
    if request.method == 'GET':
        message_id = id
        disliked(message_id)
        return redirect(f'/message/{message_id}')


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        users.check_csrf()
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template('error.html', message='Väärä käyttäjätunnus tai salasana')
            
        session['username'] = username
        return redirect("/")
  

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/')


@app.route('/message/<int:id>/deletemessage', methods=['get'])
def deletemessage(id):
    if request.method == 'GET':
        message_id = id
        delete_message(message_id)
        return redirect(f'/')






