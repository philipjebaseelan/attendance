from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Teacher(db.Model, UserMixin):

    #TABLE
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    #REFERENCES
    students = db.relationship("Student", backref="teacher")
    classes = db.relationship("Class", backref="classes")
    attends = db.relationship("Attendance", backref="attend")

class Student(db.Model):

    #TABLE
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    class_id = db.Column(db.Integer, nullable=True, default=0)
    name = db.Column(db.String(), nullable=False)
    birth = db.Column(db.String(),nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    parent = db.Column(db.String(), nullable=True)
    parent2 = db.Column(db.String(), nullable=True)
    number = db.Column(db.Integer, nullable=True)
    number2 = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(), nullable=True)
    email2 = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    attend_count = db.Column(db.Integer, nullable=True, default=0)

    #REFERENCES
    student_attends = db.relationship("Attendance", backref="student_attend")


class Class(db.Model):

    #TABLE
    __tablename__ = "class"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    name = db.Column(db.String(), nullable=False)
    lowest_age = db.Column(db.Integer, nullable=False)
    highest_age = db.Column(db.Integer, nullable=False)
    student_count = db.Column(db.Integer, default=0)
    attendance_count = db.Column(db.Integer, default=0)

    #REFERENCES
    class_attends = db.relationship("Attendance", backref="class_attend")

class Attendance(db.Model):

    #TABLE
    __tablename__ = "attendance"
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    class_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    date = db.Column(db.String(),nullable=False)
    presence = db.Column(db.String(),nullable=False)


