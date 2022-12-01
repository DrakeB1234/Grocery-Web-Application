import os
from flask import Flask, redirect, request, render_template, flash, session
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functions import login_required, allowed_file

from flask_mysqldb import MySQL

# UPLOAD path for profile pics
UPLOAD_FOLDER = 'static/images/avatars'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'svg'])


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# upload file path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        # Check to see if name and hashed password match
        for i in rows:
            if i["username"] == inputName and check_password_hash(i["hash"], inputPass):
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
    db.execute(f'SELECT * FROM users WHERE user_id = {id}')
    user = db.fetchall()
    return render_template("home.html", user=user[0])

# account settings page
@app.route("/accntsettings", methods=["GET", "POST"])
@login_required
def accntsettings():
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    id = session["user_id"]
    db.execute(f'SELECT * FROM users WHERE user_id = {id}')
    user = db.fetchall()

    if request.method == "POST":
        # information posted is for changing avatar pic
        if 'avatarFile' in request.files:
            file = request.files['avatarFile']
            username = user[0]["username"]

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect("/accntsettings")

            # format naming of filename
            file.filename = f"{username}Avatar.jpg"
            
            # allowed file checks for allowed extensions
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pathVar = UPLOAD_FOLDER + "/" + file.filename
            # if file is successful, change file path in user
            db.execute(f"UPDATE users SET avatar_path = '{pathVar}' WHERE user_id = {id}")
            mysql.connection.commit()
            # flash message then redirect
            flash("Avatar Uploaded")
            return redirect("/accntsettings")

        # information posted is for changing username
        if "userName" in request.form:
            inputName = request.form.get("userName")

            # check for valid inputs
            if not inputName:
                flash("Missing Username")
                return redirect("/accntsettings")
            if not inputName.isalnum():
                flash("Use Only Letters and Numbers")
                return redirect("/accntsettings")

            # Ensure input username is unique
            db.execute(f'SELECT username FROM users')
            usernames = db.fetchall()
            for i in usernames:
                if (i["username"] == inputName):
                    flash("Username Taken")
                    return redirect("/accntsettings")

            # Commit change in database
            db.execute(f"UPDATE users SET username = '{inputName}' WHERE user_id = {id}")
            mysql.connection.commit()

            # flash success message
            flash("Successfully changed username")

        # information posted is for changing password
        if "userPass" in request.form:
            userPass = request.form.get("userPass")
            userPassConfirm = request.form.get("userPassConfirm")

            # Check for valid input
            if not userPass:
                flash("Provide a password")
                return redirect("/accntsettings")
            if not userPass:
                flash("Provide a password")
                return redirect("/accntsettings")
            if not re.match("^[A-Za-z0-9$%#@!]*$", userPass):
                flash("Only use Letters, Numbers and ($, %, #, @, !)")
                return redirect("/accntsettings")
            if userPass != userPassConfirm:
                flash("Must have matching passwords")
                return redirect("/accntsettings")

            # Hash password
            userPass = generate_password_hash(userPass)
            # Commit change in database
            db.execute(f"UPDATE users SET hash = '{userPass}' WHERE user_id = {id}")
            mysql.connection.commit()

            return redirect("/accntsettings")

        return redirect("/accntsettings")
    
    # page is being requested
    else:
        return render_template("accntsettings.html", user=user[0])

# list page
@app.route("/list", methods=["GET", "POST"])
@login_required
def list():
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    id = session["user_id"]
    db.execute(f'SELECT * FROM users WHERE user_id = {id}')
    user = db.fetchall()

    if request.method == "POST":
        # form for adding list
        if "listTitle" in request.form:
            title = request.form.get("listTitle")
            if not title:
                flash("Provide a Title")
                return redirect("/list")
            
            if not re.match("^[A-Za-z ]*$",title):
                flash("Only use letters and spaces")
                return redirect("/list")
            
            db.execute(f'INSERT INTO listTitles (user_id, title) VALUES ({id}, "{title}");')
            mysql.connection.commit()
            flash(f"Added '{title}' to lists!")

            return redirect("/list")

        return redirect("/list")

    # method is get, page requested by user
    else:
        # get list data
        list = db.execute(f'SELECT id, title FROM listTitles WHERE user_id = {id}')
        list = db.fetchall()
        return render_template("list.html", user=user[0], list=list)

# list page
@app.route("/list/<listID>/<listTitle>", methods=["GET"])
@login_required
def list_delete(listID, listTitle):
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    id = session["user_id"]

    if not listID or not listTitle:
        flash("Provide a Title")
        return redirect("/list")
    
    if not re.match("^[A-Za-z ]*$",listTitle):
        flash("Only use letters and spaces")
        return redirect("/list")
    
    if not listID.isnumeric():
        flash("Only use numbers")
        return redirect("/list")

    # Executing sql query
    db.execute(f'DELETE FROM listTitles WHERE id = {listID} AND user_id = {id} AND title = "{listTitle}";')
    mysql.connection.commit()

    # flash message of success
    flash(f"Deleted '{listTitle}' List")
    return redirect("/list")

# view list
@app.route("/listview/<listTitle>", methods=["GET"])
@login_required
def list_view(listTitle):
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    id = session["user_id"]
    db.execute(f'SELECT * FROM users WHERE user_id = {id}')
    user = db.fetchall()
    # get all list items from selected list
    listdata = db.execute(f"""
        SELECT ld.id, title, category, item, note, amount
        FROM listData as ld
        JOIN listTitles as lt ON ld.title_id = lt.id
        JOIN listCategories as lc ON ld.category_id = lc.id 
        WHERE lt.user_id = {id} AND 
        lt.title = '{listTitle}'
        ORDER BY category DESC;
    """)
    listdata = db.fetchall()
    # check if any results
    if not listdata:
        listdata = None

    return render_template("listdata.html", user=user[0], listdata=listdata)
