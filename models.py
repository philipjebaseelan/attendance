from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Teacher(db.Model, UserMixin):


    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    students = db.relationship("Student", backref="teacher")

class Student(db.Model):

    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    name = db.Column(db.String(), nullable=False)
    birth = db.Column(db.String(),nullable=False)
    age = db.Column(db.Integer(), nullable=False)
