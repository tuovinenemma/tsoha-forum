from app import app
from flask import render_template, request, redirect, session
from db import db
import users
import messages
import reviews

@app.route("/")
def index():
    list = messages.get_list()
    return render_template("index.html", count=len(list), messages=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    headline = request.form["headline"]
    content = request.form["content"]
    if messages.send(headline, content):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut")

@app.route("/new_review")
def new_review():
    return render_template("reviews.html")

@app.route("/send_review", methods=["POST"])
def send_review():
    content = request.form["content"]
    if reviews.send_review(content):
        return redirect("/")
    else:
        return render_template("error.html", message="Palautteen lähetys ei onnistunut")

@app.route("/chat/<int:id>")
def chat(id):
    sql = "SELECT content FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    content = result.fetcone()
    return render_template("chat.html", id=id, content=content)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form['username']

        password = request.form['password']

        if not users.register(username, password):
            return render_template('error.html', message='Rekisteröinti ei onnistunut')

        return redirect('/')


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
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






