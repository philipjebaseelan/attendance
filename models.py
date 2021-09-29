from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Teacher(db.Model):


    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


