from flask import Flask, redirect, request, render_template, flash, session
from flask_mysqldb import MySQL
from functions import login_required
import re

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
@login_required
def login():
    # establish database connection
    db = mysql.connection.cursor()
    # user posted form
    if request.method == "POST":
        inputName = request.form.get("userName")
        inputPass = request.form.get("userPass")

        # check for valid inputs
        if not inputName:
            flash("Insert A Name")
            return redirect("/login")
        if not inputPass:
            flash("Insert A Password")
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
                flash(session["user_id"])
                return redirect("/")
        flash("Invalid username/password")
        return render_template("login.html")

    # user made GET request for page
    else:
        return render_template("login.html")

# home page
@app.route("/")
def home():
    return render_template("layout.html")