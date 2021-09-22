
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session

#Initialising the application & SQLite Database
app = Flask(__name__)
db = SQL("sqlite:///attendance.db")

new_user = db.execute("SELECT username FROM teachers")

@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        #Storing the values of the users details
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO teachers (name, email, username, hash) VALUES(?, ?, ?, ?)", name, email, username, password)

        return redirect("/login")
    else:
        return render_template("register.html", users=new_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("login.html")