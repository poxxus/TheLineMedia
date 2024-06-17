import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

def login_required(f):
    """
    source - https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) > 0 or (request.form.get("password") != request.form.get("confirmation")):
            return render_template("error.html", message="Invalid username or password")

        db.execute("INSERT INTO users (username, hash) VALUES (:value1, :value2)", value1 = request.form.get("username"), value2 = generate_password_hash(request.form.get("password")))

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("error.html", message="Invalid username or password")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    if request.method == "POST":
        if not request.form.get("title"):
            return render_template("error.html", message="must provide title")
        if not request.form.get("genre"):
            return render_template("error.html", message="must select a genre")
        lista = db.execute("SELECT * FROM list WHERE user_id = ?", session["user_id"])
        for entry in lista:
            if entry["title"] == request.form.get("title") and entry["genre"] == request.form.get("genre"):
                return render_template("error.html", message="title already in the list")
        db.execute("INSERT INTO list (user_id, title, genre) VALUES (:value1, :value2, :value3)", value1 = session["user_id"], value2 = request.form.get("title"), value3 = request.form.get("genre"))
        lista = db.execute("SELECT * FROM list WHERE user_id = ?", session["user_id"])
        return render_template("list.html", lista=lista)
    else:
        lista = db.execute("SELECT * FROM list WHERE user_id = ?", session["user_id"])
        return render_template("list.html", lista=lista)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        lista = db.execute("SELECT * FROM list WHERE user_id = ?", session["user_id"])
        for entry in lista:
            if entry["title"] == request.form.get("title") and entry["genre"] == request.form.get("genre"):
                db.execute("DELETE FROM list WHERE title = ? AND genre = ? AND user_id = ?", request.form.get("title"), request.form.get("genre"), session["user_id"])
                lista = db.execute("SELECT * FROM list WHERE user_id = ?", session["user_id"])
                return render_template("index.html", lista=lista)
        return render_template("error.html", message="title not in your list")
    else:
        return render_template("remove.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def theLine():
    if request.method == "GET":
        lista = db.execute("SELECT title, genre FROM list WHERE user_id = ? ORDER BY time ASC", session["user_id"])
        return render_template("index.html", lista=lista)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/")

@app.route("/get-options")
def get_options():
    selected = request.args.get('selected')
    options = db.execute("SELECT title FROM list WHERE genre = ? AND user_id = ?", (selected,), session["user_id"])
    return jsonify(options)
