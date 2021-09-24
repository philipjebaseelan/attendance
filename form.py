from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from bcrypt import gensalt, hashpw, checkpw
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo
from passlib.hash import pbkdf2_sha256

db = SQL("sqlite:///attendance.db")

def field_checking(form, field):

    entered_username = form.username.data
    entered_password = field.data

    username = db.execute("SELECT username FROM teachers WHERE username = ?", entered_username)
    hashed = db.execute("SELECT hash FROM teachers WHERE username = ?", entered_username)[0]["hash"]
    if not username:
        raise ValidationError("Incorrect username or Password.")
    elif not pbkdf2_sha256.verify(entered_password, hashed):
        raise ValidationError("Incorrect username or Password.")







class LoginUsers(FlaskForm):

    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), field_checking])




class RegisterUsers(FlaskForm):
    name = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired()])
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), Length(min=8)])
    confirm = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords do not match")])

    def validate_username(self, username):
        exist_user = db.execute("SELECT username FROM teachers WHERE username = ?", username.data)

        if exist_user:
            raise ValidationError("Username already exist.")


