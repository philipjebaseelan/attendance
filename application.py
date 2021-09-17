
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session

#Initialising the application & SQLite Database
app = Flask(__name__)
db = SQL("sqlite:///attendance.db")

@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("register.html")