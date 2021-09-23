from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from bcrypt import gensalt, hashpw, checkpw
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo


db = SQL("sqlite:///attendance.db")


class LoginUsers(FlaskForm):

    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])



    def validate_username(self, username):
        exist_user = db.execute("SELECT username FROM teachers WHERE username = ?", username.data)

        if not exist_user:
            raise ValidationError("Username does not exist.")







class RegisterUsers(FlaskForm):
    name = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired()])
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    confirm = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords do not match")])

    def validate_username(self, username):
        exist_user = db.execute("SELECT username FROM teachers WHERE username = ?", username.data)

        if exist_user:
            raise ValidationError("Username already exist.")


