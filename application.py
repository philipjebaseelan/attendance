from bcrypt import gensalt, hashpw, checkpw
from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from form import LoginUsers, RegisterUsers

#Initialising the application & SQLite Database
app = Flask(__name__)
app.config['SECRET_KEY']='LongAndRandomSecretKey'
db = SQL("sqlite:///attendance.db")




@app.route("/register", methods=["GET", "POST"])
def register():

    form_register = RegisterUsers()

    if form_register.validate_on_submit():

        #Storing the values of the users details
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        #BCRYPT encryption of password
        salt = gensalt()
        hashed = hashpw(password.encode('utf-8'), salt)

        #Storing the users data into the database.
        db.execute("INSERT INTO teachers (name, email, username, hash) VALUES(?, ?, ?, ?)", name, email, username, hashed)

        return redirect("/login")
    else:
        return render_template("register.html", form=form_register)




@app.route("/login", methods=["GET", "POST"])
def login():

    form_login = LoginUsers()

    if form_login.validate_on_submit():
        return redirect("/")
    else:
        return render_template("login.html", form=form_login)


@app.route("/")
def index():
    return render_template("layout.html")
