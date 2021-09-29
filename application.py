from flask import Flask, render_template, redirect, request,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from passlib.hash import pbkdf2_sha256
from form import *
from models import *




#Initialising the application & SQLite Database
app = Flask(__name__)
app.config["SECRET_KEY"] = "LongAndRandomSecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)

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
        hashed = pbkdf2_sha256.hash(password)

        #Storing the users data into the database.
        user = Teacher(name=name, email=email, username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
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

@app.route("/logout")
def logout():
    return redirect("/")


@app.route("/")
def index():
    return render_template("layout.html")
