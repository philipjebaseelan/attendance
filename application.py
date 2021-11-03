import os

from flask import Flask, render_template, redirect, request, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from tempfile import mkdtemp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from passlib.hash import pbkdf2_sha256
from datetime import date, datetime
from form import *
from models import *

##################################################################################################################################################################################################################################

#Initialising the application
app = Flask(__name__)
app.config["SECRET_KEY"] = "LongAndRandomSecretKey"


#Configuring Mailing Service



#Configuring SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
db = SQLAlchemy(app)


#Configuring Flask Login
login = LoginManager(app)
login.init_app(app)

#Loading a User
@login.user_loader
def load_user(id):
    return Teacher.query.get(id)

#Global Variables
states = ["Kuala Lumpur", "labuan", "Putrajaya", "Terrengganu", "Selangor", "Sarawak", "Sabah", "Perlis", "Perak", "Penang", "Pahang", "Negeri Sembilan", "Malacca", "Kelantan", "Kedah", "Johor"]


##################################################################################################################################################################################################################################


@app.route("/register", methods=["GET", "POST"])
def register():

    #initialising the form
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

        flash("Registered succesfully. Please login.")

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


        flash("Logged in Succefully!")
        return redirect("/")

    else:
        return render_template("login.html", form=form_login)

@app.route("/logout")
def logout():
    logout_user()
    flash("Successfully Logged Out")
    return redirect("/login")


@app.route("/")
def index():

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        #Passing the teachers Name
        teacher = current_user.get_id()
        teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

        #Table Header
        TABLE_HEADERS = ["#", "Name", "Class", "Attendance"]
        return render_template("index.html", teacher=teacher_object, headers=TABLE_HEADERS)

        #Fetching the students registered to the user
        students_object = db.session.query(Student).filter_by(teacher_id=teacher)
        class_object = db.session.query(Class).filter_by(teacher_id=teacher)

#############################################################STUDENTS############################################################################################
@app.route("/registrar", methods=["GET", "POST"])
def registrar():

    #Global Variables
    TABLE_HEADERS=["No.", "Name", "Class", "Age", "Parent Name", "Contact Number"]

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        if request.method == "POST":
            teacher = current_user.get_id()
            class_object = Class.query.all()
            teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()


            tag = request.form.get("tag")

            if not tag:
                return redirect("/registrar")

            search = "%{}%".format(tag)
            student_object = Student.query.filter(Student.name.like(search))

            print(student_object)
            if not student_object:
                return render_template("registrar.html", headers=TABLE_HEADERS, students="None", classes=class_object, teacher=teacher_object)
            else:
                return render_template("registrar.html", headers=TABLE_HEADERS, students=student_object, classes=class_object, teacher=teacher_object )

        else:
            teacher = current_user.get_id()
            class_object = Class.query.all()
            teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()
            student_object = Student.query.filter_by(teacher_id = teacher).order_by(Student.id.desc()).all()

            if not student_object:
                return render_template("registrar.html", headers=TABLE_HEADERS, students="None", classes=class_object, teacher=teacher_object)
            else:
                return render_template("registrar.html", headers=TABLE_HEADERS, students=student_object, classes=class_object, teacher=teacher_object )


@app.route("/add_student", methods=["GET", "POST"])
def add_student():


    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()


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
            father = request.form.get("parent_name")
            fnumber = request.form.get("parent_number")
            femail = request.form.get("parent_email")
            mother = request.form.get("parent2_name")
            mnumber = request.form.get("parent2_number")
            memail = request.form.get("parent2_email")
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


            student = Student(teacher_id=teacher, name=name, birth=dob, age=age, gender=gender, parent=father, parent2=mother, number=fnumber, number2=mnumber, email=femail, email2=memail, address=address, city=city, state=state, postcode=postcode)
            db.session.add(student)
            db.session.commit()

            flash("Succesfully Enrolled Student")
            return redirect("/registrar")

        else:
            return render_template("add-student.html", form=form_student, states=states, teacher=teacher_object)


@app.route("/detail_student/<string:id>")
def student(id):


    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()



    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:
        teacher = current_user.get_id()
        student_object = Student.query.filter_by(id=id, teacher_id=teacher)
        class_object = Class.query.all()

        return render_template("detail-student.html", students = student_object, classes=class_object, teacher=teacher_object)

@app.route("/delete_student/<string:id>")
def delete_student(id):



    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:
        teacher = current_user.get_id()
        student = db.session.query(Student).filter_by(id=id).first()
        class_id = student.class_id
        class_object = db.session.query(Class).filter_by(id=class_id).first()
        attendance = db.session.query(Attendance).filter_by(student_id=id)

        if class_id != 0:
            class_object.student_count -= 1
            db.session.merge(class_object)
            db.session.flush()


        if class_object != None:
            if class_object.student_count == 0:
                class_object.attendance_count = 0
                db.session.merge(class_object)
                db.session.flush()

        for attend in attendance:
            db.session.delete(attend)
            db.session.flush()


        db.session.delete(student)
        db.session.commit()

        flash("Successfully Removed Student")

        return redirect("/registrar")


@app.route("/edit-student/<string:id>", methods=["GET","POST"])
def edit_student(id):

    form_edit_student = EditStudents()
    student = db.session.query(Student).filter_by(id=id).first()
    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        if form_edit_student.validate_on_submit():

            student.name = request.form.get("name")
            dob = request.form.get("dob")
            option = request.form.get("gender")
            student.parent = request.form.get("parent_name")
            student.number = request.form.get("parent_number")
            student.email = request.form.get("parent_email")
            student.parent2 = request.form.get("parent2_name")
            student.number2 = request.form.get("parent2_number")
            student.email2 = request.form.get("parent2_email")
            student.address = request.form.get("address")
            student.city = request.form.get("city")
            student.state = request.form.get("state")
            student.postcode = request.form.get("postcode")

            #Calculating the age
            today = datetime.today()
            birthdate = datetime.strptime(dob, '%Y-%m-%d')
            student.age = today.year - birthdate.year
            student.birth = dob

            #Storing the gender
            if option == "option1":
                student.gender = "Male"
                db.session.flush()
            else:
                student.gender = "Female"
                db.session.flush()

            db.session.merge(student)
            db.session.commit()

            flash("Succesfully saved changes.")

            return redirect("/detail_student/"+id)

        else:
            return render_template("edit-student.html", student=student, form=form_edit_student, states=states, teacher=teacher_object)


#####################################################CLASSES##########################################################################################################

@app.route("/class")
def classes():

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        TABLE_HEADERS=["No.", "Class Name", "Age Group", "No. of Students"]
        teacher = current_user.get_id()
        class_object = Class.query.filter_by(teacher_id = teacher).order_by(Class.id.desc()).all()
        return render_template("class.html", headers=TABLE_HEADERS, classes=class_object, teacher=teacher_object)



@app.route("/add_class", methods=["GET", "POST"])
def add_class():

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

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

            flash("Succesfully Created Class")
            return redirect("/class")

        else:
            return render_template("add-class.html", form=form_class, teacher=teacher_object)


@app.route("/detail_class/<string:id>")
def detail_class(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        TABLE_HEADERS=["No.", "Name", "Age", "Parent Name", "Contact Number", "Attendance"]
        teacher = current_user.get_id()
        class_object = Class.query.filter_by(id = id).first()

        students = Student.query.filter_by(class_id=id, teacher_id=teacher)
        class_attendance = Attendance.query.filter_by(class_id=id, teacher_id=teacher)
        return render_template("detail-class.html", classes=class_object, headers=TABLE_HEADERS, students=students, attendances=class_attendance, teacher=teacher_object)

@app.route("/delete-class/<string:id>")
def delete_class(id):


    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        class_object = db.session.query(Class).filter_by(id=id).first()

        if class_object.student_count == 0:
            db.session.delete(class_object)
            db.session.commit()

        elif class_object.student_count != 0:
            students = db.session.query(Student).filter_by(class_id=id)
            attendance= db.session.query(Attendance).filter_by(class_id=id)

            for attend in attendance:
                db.session.delete(attend)
                db.session.flush()

            for student in students:
                student.class_id = 0
                student.attend_count = 0
                db.session.merge(student)
                db.session.flush()

            db.session.delete(class_object)
            db.session.commit()

        flash("Succesfully removed class.")
        return redirect("/class")

@app.route("/add_student_class/<string:id>")
def add_student_class(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:

            TABLE_HEADERS=["#","Name", "Age"]
            teacher = current_user.get_id()
            null_students = Student.query.filter_by(teacher_id=teacher, class_id = 0)
            return render_template("add-student-class.html", students=null_students, headers=TABLE_HEADERS,ident=id, teacher=teacher_object)


@app.route("/added_student_class/<string:id>", methods=["POST"])
def added_student_class(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        teacher = current_user.get_id()
        students = db.session.query(Student).filter_by(teacher_id=teacher, class_id=0)
        class_object = db.session.query(Class).filter_by(id=id, teacher_id=teacher).first()
        class_id = id


        for student in students:
            status = request.form.get("btncheck"+str(student.id))

            if status == "Add":
                class_inc = db.session.query(Class).filter_by(id=class_id, teacher_id=teacher).first()
                student.class_id = class_id
                class_inc.student_count += 1
                db.session.merge(student)
                db.session.merge(class_inc)
                db.session.commit()


        return redirect("/detail_class/" +class_id)


@app.route("/remove-student-class/<string:id>", methods=["GET","POST"])
def remove_student_class(id):

    #Variables
    TABLE_HEADERS = ["#", "Name"]
    students = db.session.query(Student).filter_by(class_id=id).all()
    class_object = db.session.query(Class).filter_by(id=id).first()
    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        if request.method == "POST":

            for student in students:
                status = request.form.get("btncheck"+str(student.id))


                if status == "Remove":
                    class_object.student_count -= 1
                    student.class_id = 0
                    db.session.merge(class_object)
                    db.session.merge(student)
                    db.session.flush()

                    if student.attend_count != 0:
                        attends = db.session.query(Attendance).filter_by(student_id=student.id, class_id=id).all()
                        student.attend_count = 0
                        db.session.merge(student)
                        db.session.flush()

                        for attend in attends:
                            db.session.delete(attend)
                            db.session.flush()

                    if class_object.student_count == 0:
                        class_object.attendance_count = 0
                        db.session.merge(class_object)
                        db.session.flush()

                    db.session.commit()

            flash("Succesfully removed Student's from Class.")

            return redirect("/detail_class/" +id)

        else:
            return render_template("remove-student-class.html", headers=TABLE_HEADERS, students=students, classes=class_object, teacher=teacher_object)

@app.route("/detail-class-student/<string:id>")
def detail_class_student(id):

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        teacher = current_user.get_id()
        teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()
        student_object = Student.query.filter_by(id=id, teacher_id=teacher)
        class_object = Class.query.all()

        return render_template("detail-class-student.html", students=student_object, classes=class_object, teacher=teacher_object)

@app.route("/detail-class-edit-student/<string:id>", methods=["GET","POST"])
def detail_class_edit_student(id):

    form_edit_student = EditStudents()
    student = db.session.query(Student).filter_by(id=id).first()
    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")
    else:
        if form_edit_student.validate_on_submit():

            student.name = request.form.get("name")
            dob = request.form.get("dob")
            option = request.form.get("gender")
            student.parent = request.form.get("parent_name")
            student.number = request.form.get("parent_number")
            student.email = request.form.get("parent_email")
            student.parent2 = request.form.get("parent2_name")
            student.number2 = request.form.get("parent2_number")
            student.email2 = request.form.get("parent2_email")
            student.address = request.form.get("address")
            student.city = request.form.get("city")
            student.state = request.form.get("state")
            student.postcode = request.form.get("postcode")

            #Calculating the age
            today = datetime.today()
            birthdate = datetime.strptime(dob, '%Y-%m-%d')
            student.age = today.year - birthdate.year
            student.birth = dob

            #Storing the gender
            if option == "option1":
                student.gender = "Male"
                db.session.flush()
            else:
                student.gender = "Female"
                db.session.flush()

            db.session.merge(student)
            db.session.commit()

            flash("Succesfully saved changes.")

            return redirect("/detail-class-student/"+ str(student.id))

        else:
            return render_template("detail-class-edit-student.html", student=student, form=form_edit_student, states=states, teacher=teacher_object)


#####################################################ATTENDANCE#####################################################################

@app.route("/take-attendance/<string:id>")
def take_attendance(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        form_attend = TakeAttendance()
        TABLE_HEADERS = ["No.", "Student Name", "Attendance"]
        students = db.session.query(Student).filter_by(class_id=id)
        return render_template("take-attendance.html", ident=id, form=form_attend, headers=TABLE_HEADERS, students=students, teacher=teacher_object)



@app.route("/taken-attendance/<string:id>", methods=["POST"])
def taken_attendance(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:

        date = request.form.get("date")
        teacher = current_user.get_id()
        students = db.session.query(Student).filter_by(class_id=id)

        for student in students:
            attend = request.form.get("btnradio"+str(student.id))

            if attend == "option1":
                presence = "Present"
                attendance_object = Attendance(teacher_id=teacher, class_id=id, student_id=student.id, date=date, presence=presence)
                attend = db.session.query(Student).filter_by(id=student.id).first()
                attend.attend_count += 1
                db.session.add(attendance_object)
                db.session.merge(attend)
                db.session.commit()

            else:
                presence = "Absent"
                attendance_object = Attendance(teacher_id=teacher, class_id=id, student_id=student.id, date=date, presence=presence)
                db.session.add(attendance_object)
                db.session.commit()


        class_inc = Class.query.filter_by(id=id).first()
        class_inc.attendance_count += 1
        db.session.merge(class_inc)
        db.session.commit()

        flash("Attendance Taken")

        return redirect("/detail_class/"+id)

@app.route("/detail_attendance/<string:id>")
def detail_attendance(id):

    teacher = current_user.get_id()
    teacher_object = db.session.query(Teacher).filter_by(id=teacher).first()

    #Ensuring User is logged in
    if not current_user.is_authenticated:
        return redirect("/login")

    else:
        TABLE_HEADERS = ["No.", "Date", "Attendnace"]
        student_object = db.session.query(Student).filter_by(id=id).first()
        class_id = student_object.class_id
        attendance_object = db.session.query(Attendance).filter_by(student_id=id).order_by(Attendance.date.desc())
        new_attendance = db.session.query(Attendance).filter_by(class_id=class_id).group_by(Attendance.date)


        return render_template("detail-attendance.html", headers=TABLE_HEADERS, attendances=attendance_object, student=student_object, new_student=new_attendance, teacher=teacher_object)
