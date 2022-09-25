from app import app
from flask import render_template, request, redirect
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
			return render_template("error.html", message="Väärä tunnus tai salasana!")
		return redirect("/")