from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from passlib.hash import pbkdf2_sha256
from datetime import date, datetime
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

#Global Variables
states = ["Kuala Lumpur", "labuan", "Putrajaya", "Terrengganu", "Selangor", "Sarawak", "Sabah", "Perlis", "Perak", "Penang", "Pahang", "Negeri Sembilan", "Malacca", "Kelantan", "Kedah", "Johor"]




@app.route("/register", methods=["GET", "POST"])
def register():

    form_register = RegisterUsers()

    if form_register.validate_on_submit():

        #Storing the values of the users details
        name = request.form.get("name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        #Passlib encryption of password
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

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    return render_template("layout.html")

@app.route("/registrar")
def registrar():

    TABLE_HEADERS=["Name","Class", "Age", "Parent Name", "Contact Number"]

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        teacher = current_user.get_id()
        student_object = Student.query.filter_by(teacher_id = teacher).order_by(Student.id.desc()).all()
        return render_template("registrar.html", headers=TABLE_HEADERS, students=student_object)


@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:

        form_student = AddStudents()
        today = date.today()

        if form_student.validate_on_submit():

            teacher=current_user.get_id()

            name = request.form.get("name")
            dob = request.form.get("dob")
            option = request.form.get("gender")
            parent = request.form.get("parent_name")
            number = request.form.get("parent_number")
            email = request.form.get("parent_email")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            postcode = request.form.get("postcode")


            #Calculating the age
            today = datetime.today()
            birthdate = datetime.strptime(dob, '%Y-%m-%d')
            age = today.year - birthdate.year

            #Storing the gender
            if option == "option1":
                gender = "Male"
            else:
                gender = "Female"



            student = Student(teacher_id=teacher, name=name, birth=dob, age=age, parent=parent, number=number, email=email, address=address, city=city, state=state, postcode=postcode)
            db.session.add(student)
            db.session.commit()

            print(gender)
            return redirect("/registrar")

        else:
            return render_template("add-student.html", form=form_student, states=states)


@app.route("/detail_student/<string:id>")
def student(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:

        teacher = current_user.get_id()

        student_object = Student.query.filter_by(id=id, teacher_id=teacher)

        return render_template("detail-student.html", students = student_object)

@app.route("/delete_student/<string:id>")
def delete_student(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        teacher = current_user.get_id()
        student = db.session.query(Student).filter(id==id).first()

        db.session.delete(student)
        db.session.commit()


        return redirect("/registrar")



@app.route("/class")
def classes():

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        TABLE_HEADERS=["Class Name", "Age Group", "No. of Students"]



        teacher = current_user.get_id()
        class_object = Class.query.filter_by(teacher_id = teacher).order_by(Class.id.desc()).all()




        return render_template("class.html", headers=TABLE_HEADERS, classes=class_object)



@app.route("/add_class", methods=["GET", "POST"])
def add_class():

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        form_class = AddClass()

        if form_class.validate_on_submit():

            teacher = current_user.get_id()
            name = request.form.get("name")
            lage = request.form.get("lage")
            hage = request.form.get("hage")

            class_object = Class(teacher_id=teacher, name=name, lowest_age=lage, highest_age=hage)
            db.session.add(class_object)
            db.session.commit()
            return redirect("/class")

        else:
            return render_template("add-class.html", form=form_class)


@app.route("/detail_class/<string:id>")
def detail_class(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        TABLE_HEADERS=["Name", "Age", "Parent Name", "Contact Number", "Attendance"]
        teacher = current_user.get_id()
        class_object = Class.query.filter_by(id = id).first()

        students = Student.query.filter_by(class_id=id, teacher_id=teacher)

        return render_template("detail-class.html", classes=class_object, headers=TABLE_HEADERS, students=students)


@app.route("/add_student_class/<string:id>")
def add_student_class(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
            val = None
            null_students = Student.query.filter_by(class_id = None)
            return render_template("add-student-class.html", students=null_students, ident=id)

@app.route("/added_student_class/<string:id>", methods=["POST"])
def added_student_class(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:
        name = request.form.get("students")
        teacher = current_user.get_id()
        class_id = id

        student = Student.query.filter_by( name=name, teacher_id=teacher).first()
        class_inc = Class.query.filter_by(id=class_id, teacher_id=teacher).first()
        student.class_id = class_id
        class_inc.count += 1
        db.session.merge(student)
        db.session.merge(class_inc)
        db.session.commit()

        return redirect("/detail_class/" +id)

