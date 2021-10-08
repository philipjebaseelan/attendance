from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, RadioField
from wtforms.validators import ValidationError, InputRequired, Length, EqualTo
from wtforms.fields.html5 import DateField
from passlib.hash import pbkdf2_sha256
from models import *

#Global Validation

def login_checking(form, field):

    entered_username = form.username.data
    entered_password = field.data

    user_object = Teacher.query.filter_by(username=entered_username).first()
    if not user_object:
        raise ValidationError("Invalid Username or Password.")
    elif not pbkdf2_sha256.verify(entered_password, user_object.password):
        raise ValidationError("Invalid Username or Password.")

def class_age_checking(form, field):

    lowest = form.lage.data
    highest = field.data

    if lowest >= highest:
        raise ValidationError("Incorrect Age Group Format")

#Forms

#login Form
class LoginUsers(FlaskForm):

    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), login_checking])

#Registration Form
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

#Add Student Form
class AddStudents(FlaskForm):
    name = StringField(validators=[InputRequired()])
    dob = DateField(validators=[InputRequired()])
    parent_name = StringField(validators=[InputRequired()])
    parent_number = IntegerField(validators=[InputRequired()])
    parent_email = StringField(validators=[InputRequired()])
    parent2_name = StringField(validators=[InputRequired()])
    parent2_number = IntegerField(validators=[InputRequired()])
    parent2_email = StringField(validators=[InputRequired()])
    address = StringField(validators=[InputRequired()])
    city = StringField(validators=[InputRequired()])
    postcode = IntegerField(validators=[InputRequired()])

    def validate_state(self, state):
        if state.data == "State":
            raise ValidationError("Please select your state.")

#Add Class Form
class AddClass(FlaskForm):
    name = StringField(validators=[InputRequired()])
    lage = IntegerField(validators=[InputRequired()])
    hage = IntegerField(validators=[InputRequired(), class_age_checking])

    def validate_name(self, name):
        class_object = Class.query.filter_by(name=name.data).first()

        if class_object:
            raise ValidationError("Username already exist.")
