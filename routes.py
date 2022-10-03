from app import app
from flask import render_template, request, redirect, session
from db import db
import users

@app.route("/")
def index():
    return render_template("index.html")


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

@app.route("/forum")
def forum():
    return render_template("forum.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users.register(username, password)
    return redirect("/forum")
        

@app.route("/logout")
def logout():
    return redirect('/login')

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/")


