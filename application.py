from flask import Flask, render_template

#Initialising the application & SQLite Database
app = Flask(__name__)
db = SQL("sqlite:///attendance.db")

@app.route("/")
def index():
    return render_template("layout.html")