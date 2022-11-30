from flask import Flask, redirect, request, render_template, flash, session
from functools import wraps
import re
from functions import login_required

from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# database conn
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '791384265Templegrd'
app.config['MYSQL_HOST'] = 'main-database.cbhkqg0xerfz.us-east-2.rds.amazonaws.com'
app.config['MYSQL_DB'] = 'database1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



"""
    ~~~TODO~~~
    disable cache
    connect AWS database

"""

# login page
@app.route("/login", methods=["POST", "GET"])
def login():
    # establish database connection
    db = mysql.connection.cursor()
    # user posted form
    if request.method == "POST":
        inputName = request.form.get("userName")
        inputPass = request.form.get("userPass")

        # check for valid inputs
        if not inputName:
            flash("Missing Username")
            return redirect("/login")
        if not inputPass:
            flash("Missing Password")
            return redirect("/login")
        if not inputName.isalnum():
            flash("Use Only Letters and Numbers")
            return redirect("/login")
        if not inputName.isalnum():
            flash("Use Only Letters and Numbers")
            return redirect("/login")
        if not re.match("^[A-Za-z0-9$%#@!]*$",inputPass):
            flash("Only use Letters, Numbers and ($, %, #, @, !)")
            return redirect("/login")
        
        # fetch all users
        db.execute('''SELECT * FROM users''')
        rows = db.fetchall()
        # check to see if name and pass match
        for i in rows:
            if i["username"] == inputName and i["hash"] == inputPass:
                # if match, redirect to homepage and set session variable 
                flash("Logged In")
                session["user_id"] = i["user_id"]
                return redirect("/")
        flash("Invalid username/password")
        return render_template("login.html")

    # user made GET request for page
    else:
        return render_template("login.html")

# logout
@app.route("/logout", methods=["GET"])
def logout():
    session["user_id"] = None
    flash("Logged Out")
    return redirect("/")

# home page
@app.route("/")
@login_required
def home():
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    id = session["user_id"]
    db.execute(f'''SELECT * FROM users WHERE user_id = {id}''')
    user = db.fetchall()
    return render_template("home.html", user=user[0])

# list page
@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    # establish database connection
    db = mysql.connection.cursor()
    if request.method == "POST":
        # Post from selecting list
        if "nameTitle" in request.form:
            title = request.form.get("nameTitle")
            if not title:
                flash("Provide a List to View")
                return redirect("/list")
                
            flash(title)

        return redirect("/list")
    else:
        # get user data
        id = session["user_id"]
        db.execute(f'''SELECT * FROM users WHERE user_id = {id}''')
        user = db.fetchall()
        # get list data
        db.execute(f'''SELECT * FROM listTitles WHERE user_id = {id}''')
        list = db.fetchall()
        return render_template("list.html", user=user[0], list=list)