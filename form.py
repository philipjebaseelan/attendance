from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo
from passlib.hash import pbkdf2_sha256
from models import *

#Global Variables
states = ["State", "Kuala Lumpur", "labuan", "Putrajaya", "Terrengganu", "Selangor", "Sarawak", "Sabah", "Perlis", "Perak", "Penang", "Pahang", "Negeri Sembilan", "Malacca", "Kelantan", "Kedah", "Johor"]

#Global Validation

def login_checking(form, field):

    entered_username = form.username.data
    entered_password = field.data

    user_object = Teacher.query.filter_by(username=entered_username).first()
    if not user_object:
        raise ValidationError("Invalid Username or Password.")
    elif not pbkdf2_sha256.verify(entered_password, user_object.password):
        raise ValidationError("Invalid Username or Password.")




#Forms

class LoginUsers(FlaskForm):

    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), login_checking])

class RegisterUsers(FlaskForm):
    name = StringField(validators=[InputRequired()])
    email = StringField(validators=[InputRequired()])
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, message ="Password needs to be at least 8 characters long")])
    confirm = PasswordField(validators=[InputRequired(), EqualTo('password', message="Passwords do not match")])

    def validate_username(self, username):
        user_object = Teacher.query.filter_by(username=username.data).first()

        if user_object:
            raise ValidationError("Username already exist.")

class AddStudents(FlaskForm):
    name = StringField(validators=[InputRequired()])
    dob = DateField(validators=[InputRequired()])
    parent_name = StringField(validators=[InputRequired()])
    parent_number = IntegerField(validators=[InputRequired()])
    parent_email = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    city = StringField(validators=[InputRequired()])
    state = SelectField(validators=[InputRequired()], choices=[(state) for state in states])
    postcode = IntegerField(validators=[InputRequired()])