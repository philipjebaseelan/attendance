from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from passlib.hash import pbkdf2_sha256
from form import *
from models import *




#Initialising the application
app = Flask(__name__)
app.config["SECRET_KEY"] = "LongAndRandomSecretKey"

#Configuring SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)

#Configuring Flask Login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    return Teacher.query.get(id)


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

        #logging in the user
        username = request.form.get("username")
        user_object = Teacher.query.filter_by(username=username).first()
        login_user(user_object)
        return redirect("/")

    else:
        return render_template("login.html", form=form_login)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
def index():

    if not current_user.is_authenticated:
        return redirect("/login")


    return render_template("layout.html")
