import os
from flask import Flask, redirect, request, render_template, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functions import login_required, allowed_file, save_change_time
from datetime import datetime, timedelta

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

# function for getting user data
def user_info(id):
    # establish database connection
    db = mysql.connection.cursor()
    # get user data
    db.execute(f'SELECT * FROM users WHERE user_id = {id}')
    session["user"] = db.fetchall()
    session["user_id"] = id
    # check meal planner function
    meal_planner_check()


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
            flash("Missing Username", "User-Error")
            return redirect("/login")
        if not inputPass:
            flash("Missing Password", "User-Error")
            return redirect("/login")
        if not inputName.isalnum():
            flash("Use Only Letters and Numbers", "User-Error")
            return redirect("/login")
        if not inputName.isalnum():
            flash("Use Only Letters and Numbers", "User-Error")
            return redirect("/login")
        if not re.match("^[A-Za-z0-9$%#@!]*$",inputPass):
            flash("Only use Letters, Numbers and ($, %, #, @, !)", "User-Error")
            return redirect("/login")
        
        # fetch all users
        db.execute('SELECT * FROM users')
        rows = db.fetchall()
        # Check to see if name and hashed password match
        for i in rows:
            if i["username"] == inputName and check_password_hash(i["hash"], inputPass):
                # if match, redirect to homepage and set session variable 
                flash("Logged In", "Success")
                user_info(i["user_id"])
                return redirect("/")
        flash("Invalid username/password", "User-Error")
        return render_template("login.html")

    # user made GET request for page
    else:
        return render_template("login.html")

# logout
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session["user_id"] = None
    flash("Logged Out", "Success")
    return redirect("/")

# home page
@app.route("/")
@login_required
def home():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    user = session.get("user")
    id = session.get("user_id")

    # get user stats

    # adding list count
    db.execute(f'''
    SELECT count(title) as listCount
    FROM listTitles 
    WHERE user_id = {id} 
    ORDER BY title ASC
    ''')
    grocery = db.fetchall()

    # adding item count 
    db.execute(f'''
    SELECT count(item) as itemCount
    FROM listData as ld
    JOIN listTitles as lt ON lt.id = ld.title_id
    WHERE lt.user_id = {id} 
    ''')
    grocery += db.fetchall()

    return render_template("home.html", user=user[0], url=request.path, grocery=grocery, grocerytime=session.get("grocery_time"))

# account settings page
@app.route("/accntsettings", methods=["GET", "POST"])
@login_required
def accntsettings():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    user = session.get("user")
    id = session.get("user_id")

    if request.method == "POST":
        # information posted is for changing avatar pic
        if 'avatarFile' in request.files:
            file = request.files['avatarFile']
            username = user[0]["username"]

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file', "User-Error")
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
            flash("Avatar Uploaded", "Success")
            return redirect("/accntsettings")

        # information posted is for changing username
        if "userName" in request.form:
            inputName = request.form.get("userName")

            # check for valid inputs
            if not inputName:
                flash("Missing Username", "User-Error")
                return redirect("/accntsettings")
            if not inputName.isalnum():
                flash("Use Only Letters and Numbers", "User-Error")
                return redirect("/accntsettings")

            # Ensure input username is unique
            db.execute(f'SELECT username FROM users')
            usernames = db.fetchall()
            for i in usernames:
                if (i["username"] == inputName):
                    flash("Username Taken", "User-Error")
                    return redirect("/accntsettings")

            # Commit change in database
            db.execute(f"UPDATE users SET username = '{inputName}' WHERE user_id = {id}")
            mysql.connection.commit()

            # flash success message
            flash("Successfully changed username", "Success")
            # get new user info
            user_info(id)

        # information posted is for changing password
        if "userPass" in request.form:
            userPass = request.form.get("userPass")
            userPassConfirm = request.form.get("userPassConfirm")

            # Check for valid input
            if not userPass:
                flash("Provide a password", "User-Error")
                return redirect("/accntsettings")
            if len(userPass) < 7:
                flash("Need at least 7 characters", "User-Error")
                return redirect("/login")
            if not re.match("^[A-Za-z0-9$%#@!]*$", userPass):
                flash("Only use Letters, Numbers and ($, %, #, @, !)", "User-Error")
                return redirect("/accntsettings")
            if userPass != userPassConfirm:
                flash("Must have matching passwords", "User-Error")
                return redirect("/accntsettings")

            # Hash password
            userPass = generate_password_hash(userPass)
            # Commit change in database
            db.execute(f"UPDATE users SET hash = '{userPass}' WHERE user_id = {id}")
            mysql.connection.commit()
            # flash success message
            flash("Successfully changed password", "Success")
            # get new user info
            user_info(id)

            return redirect("/accntsettings")

        return redirect("/accntsettings")
    
    # page is being requested
    else:
        return render_template("accntsettings.html", user=user[0], url=request.path)

# list page
@app.route("/list", methods=["GET"])
@login_required
def list():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    user = session.get("user")
    id = session["user_id"]

    # get list data
    list = db.execute(f'SELECT id, title FROM listTitles WHERE user_id = {id} ORDER BY title ASC')
    list = db.fetchall()
    return render_template("list.html", user=user[0], list=list, url=request.path)

# list modifcation route
@app.route("/listmod", methods=["POST"])
@login_required
def list_mod():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # if request is to add form
    if "listAdd" in request.form:
        titleName = request.form.get("listAdd")

        if not titleName:
            flash("Provide a Title", "User-Error")
            return redirect("/list")

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9 ]*$",titleName):
            flash("Only use numbers, letters, and spaces", "User-Error")
            return redirect("/list")

        # checking for valid amount of text
        if len(titleName) < 3 or len(titleName) > 20:
            flash("Use 3 or 20 characters", "User-Error")
            return redirect("/list")

        # Executing sql query
        db.execute(f'''
            INSERT INTO listTitles (user_id, title) 
            VALUES ({id}, '{titleName}')
            ''')
        mysql.connection.commit()

        # flash message of success
        flash("Added New List", "Success")
        return redirect("/list")

    # setting input to var
    listID = request.form.get("listID")

    # checking for valid ID
    if not listID:
        flash("Provide a ID", "User-Error")
        return redirect("/list")

    if not listID.isnumeric():
        flash("Only use numbers", "User-Error")
        return redirect("/list")

    # if request is to delete form
    if "listDel" in request.form:

        # Executing sql query to delete list data with title id
        db.execute(f'''
            DELETE ld 
            FROM listData as ld
            JOIN listTitles as lt ON ld.title_id = lt.id
            WHERE ld.title_id = {listID} AND 
            lt.user_id = {id}
        ''')
        mysql.connection.commit()

        # Executing sql query to delete list
        db.execute(f'DELETE FROM listTitles WHERE id = {listID} AND user_id = {id}')
        mysql.connection.commit()

        # flash message of success
        flash("Deleted List and all items within", "Success")
        return redirect("/list")

    # if request is to delete form
    if "listEdit" in request.form:

        # get new title name from input
        titleName = request.form.get("listEdit")

        # checking for valid title
        if not titleName:
            flash("Provide a ID", "User-Error")
            return redirect("/list")

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9 ]*$",titleName):
            flash("Only use numbers, letters, and spaces", "User-Error")
            return redirect("/list")

        # checking for valid amount of text
        if len(titleName) < 3 or len(titleName) > 20:
            flash("Use 3 or 20 characters", "User-Error")
            return redirect("/list")

        # Executing sql query
        db.execute(f"UPDATE listTitles SET title = '{titleName}' WHERE id = {listID} AND user_id = {id}")
        mysql.connection.commit()

        # flash message of success
        flash("Edited List", "Success")
        return redirect("/list")

    return redirect("/list")


# view list
@app.route("/listview/<listTitle> <listID>", methods=["GET"])
@login_required
def list_view(listTitle, listID):
    # establish database connection
    db = mysql.connection.cursor()

    # get user details
    user = session.get("user")
    id = session["user_id"]

    if not listID:
        flash("Need to provide more Info", "User-Error")
        return(redirect("/list"))

    # get all list items from selected list
    listdata = db.execute(f"""
        SELECT ld.id, title, category, color as catColor, item, note, amount
        FROM listData as ld
        JOIN listTitles as lt ON ld.title_id = lt.id
        JOIN listCategories as lc ON ld.category_id = lc.id 
        WHERE lt.user_id = {id} AND 
        lt.title = '{listTitle}' AND
        lt.id = {listID}
        ORDER BY orderNum, category ASC, item ASC;
    """)
    listdata = db.fetchall()

    # get all categories
    db.execute(f'SELECT category FROM listCategories ORDER BY orderNum, category;')
    listcat = db.fetchall()

    # save current path to return back to
    session["list_path"] = request.path
    return render_template("listview.html", user=user[0], listdata=listdata, listcat=listcat, url=request.path, listTitle=listTitle)

# view list
@app.route("/listviewmod", methods=["POST"])
@login_required
def list_view_mod():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # item is requested to be added 
    if "itemAddItem" in request.form:
        listTitle = request.form.get("listTitle")
        itemCat = request.form.get("itemAddCat")
        itemName = request.form.get("itemAddItem")
        itemNote = request.form.get("itemAddNote")
        itemAmnt = request.form.get("itemAddAmnt")

        # validating input    
        if not itemCat or not itemName or not itemAmnt or not listTitle:
            flash("Missing Required Input", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9 ]*$",listTitle):
            flash("Only use numbers, letters, and spaces for title", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z][a-zA-Z ]*$",itemCat):
            flash("Only use letters and spaces for category", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z][a-zA-Z ]*$",itemName):
            flash("Only use letters and spaces for item", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9 ]*$",itemNote) and itemNote != "":
            flash("Only use numbers, letters, and spaces for notes", "User-Error")
            return redirect(session["list_path"])

        if not itemAmnt.isnumeric():
            flash("Only use numbers for amount", "User-Error")
            return redirect(session["list_path"])

        # convert amnt to int
        itemAmnt = int(itemAmnt)
        if itemAmnt < 1 or itemAmnt > 99:
            flash("Only use (0 - 99) for amount", "User-Error")
            return redirect(session["list_path"])

        # changing note to blank string if none type
        if itemNote == None:
            itemNote = ""

        # Executing sql query
        db.execute(f'''
            INSERT INTO listData (title_id, category_id, item, note, amount) 
            VALUES ((SELECT id
                    FROM listTitles
                    WHERE title = "{listTitle}" AND 
                    user_id = {id}
                    ),
                (SELECT id
                    FROM listCategories
                    WHERE category = "{itemCat}"
                    ),
            "{itemName}", "{itemNote}", {itemAmnt})
        ''')
        mysql.connection.commit()

        # save time of change
        save_change_time() 
        # redirect for success (no flash messaging for better UX)
        return redirect(session["list_path"])

    # item is requested to be edited 
    if "itemEditItem" in request.form:
        itemID = request.form.get("itemID")
        amnt = request.form.get("itemEditAmnt")
        item = request.form.get("itemEditItem")
        note = request.form.get("itemEditNote")

        # validating input    
        if not itemID or not amnt or not item:
            flash("Missing Required Input", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z][a-zA-Z ]*$",item):
            flash("Only use letters and spaces for item", "User-Error")
            return redirect(session["list_path"])

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9 ]*$",note) and note != "":
            flash("Only use numbers, letters, and spaces for notes", "User-Error")
            return redirect(session["list_path"])

        if not amnt.isnumeric():
            flash("Only use numbers for amount", "User-Error")
            return redirect(session["list_path"])

        # convert amnt to int
        amnt = int(amnt)
        if amnt < 1 or amnt > 99:
            flash("Only use (0 - 99) for amount", "User-Error")
            return redirect(session["list_path"])

        if not itemID.isnumeric():
            flash("Invalid use of number", "User-Error")
            return redirect(session["list_path"])

        # Executing sql query
        db.execute(f'''
            UPDATE listData as ld
            JOIN listTitles as lt ON ld.title_id = lt.id
            SET item = '{item}', note = '{note}', amount = {amnt}
            WHERE ld.id = {itemID} AND 
            user_id = {id};
        ''')
        mysql.connection.commit()

        # save time of change
        save_change_time() 
        # flash message of success
        flash("Edited Item", "Success")
        return redirect(session["list_path"])

    # item is requested to be removed 
    if "itemDel" in request.form:
        itemID = request.form.get("itemDel")

        # validate input
        if not itemID:
            flash("Provide an ID", "User-Error")
            return redirect(session["list_path"])

        if not itemID.isnumeric():
            flash("Only use Numbers", "User-Error")
            return redirect(session["list_path"])

        # Executing sql query
        db.execute(f'''
            DELETE ld 
            FROM listData as ld
            JOIN listTitles as lt ON ld.title_id = lt.id
            WHERE ld.id = {itemID} AND 
            lt.user_id = {id}
        ''')
        mysql.connection.commit()

        # save time of change
        save_change_time() 
        # flash message of success
        flash("Deleted Item", "Success")
        return redirect(session["list_path"])

# mealplanner page
@app.route("/mealplanner", methods=["GET"])
@login_required
def mealplan():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]
    # get user details
    user = session.get("user")

    # getting users meal planner
    db.execute(f'''
    SELECT id, date, DAY(date) as day, MONTH(date) as month, weekday, meal
    FROM mealPlanner 
    WHERE user_id = {id} 
    ORDER BY date ASC
    ''')
    mealplan = db.fetchall()

    if mealplan == ():
        # nothing in planner, call adder function
        add_meal_planner()
        flash("added meal planner", "Success")
        return redirect("/")

    # get current month
    month = mealplan[0]["date"].strftime("%B")

    # check meal planner function
    meal_planner_check()

    return render_template("mealplanner.html", user=user[0], url=request.path, mealplan=mealplan, month=month)

# mealplanner mod page
@app.route("/mealplannermod", methods=["POST"])
@login_required
def mealplanmod():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # meal is requested to be edited 
    if "mealEditItem" in request.form:
        mealID = request.form.get("mealID")
        meal = request.form.get("mealEditItem")

        if not mealID or not meal:
            flash("Fill All Required Inputs", "User-Error")
            return redirect("/mealplanner")

        if not re.match("^[a-zA-Z][a-zA-Z ]*$", meal):
            flash("Only use letters and spaces for meal", "User-Error")
            return redirect("/mealplanner")

        if not mealID.isnumeric():
            flash("Only use numbers", "User-Error")
            return redirect("/mealplanner")
        
        # Executing sql query
        db.execute(f'''
            UPDATE mealPlanner
            SET meal = '{meal}'
            WHERE id = {mealID} AND 
            user_id = {id}
        ''')
        mysql.connection.commit()

        # flash message of success
        flash("Edited Meal", "Success")
        return redirect("/mealplanner")

    return redirect("/mealplanner")

@app.errorhandler(404)
def page_not_found(e):
    flash("Page not Found", "Server-Error")
    return redirect('/')

@app.errorhandler(500)
def internal_error(e):
    flash("Internal Error, Contact Admin", "Server-Error")
    return redirect('/')


# extra functions
def meal_planner_check():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # get current date
    now = datetime.now()
    curDay = now.strftime("%d")

    # get value of last day in planner
    db.execute(f'''
        SELECT date
        FROM mealPlanner
        WHERE user_id = {id}
        ORDER BY date DESC
        LIMIT 1;
    ''')
    curMeals = db.fetchall()
    print(curMeals)

    if curMeals == ():
        # nothing in planner, call adder function
        add_meal_planner()
        flash("added meal planner", "Success")
        return redirect("/")

    # convert current day to int and get current day
    curDay = int(curDay)
    curMeals = int(curMeals[0]["date"].strftime("%d"))

    # if current day is next after the last set in planner
    if curDay >= (curMeals + 1):
        # Executing sql query
        db.execute(f'''
	        UPDATE mealPlanner 
            SET date = DATE_ADD(date, INTERVAL 7 DAY)
            WHERE user_id = {id}
        ''')
        mysql.connection.commit()

        # flash message
        flash("Reset Meal Planner", "Success")

    return

def add_meal_planner():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # get current date
    now = datetime(2022, 12, 10)

    for i in range(7):
        now = now + timedelta(days=1)
        weekday = now.strftime("%a").upper()
        # Executing sql query
        db.execute(f'''
            INSERT INTO mealPlanner (user_id, date, weekday, meal)
            VALUES ({id}, '{now}', '{weekday}', "Unset")
        ''')
        mysql.connection.commit()
    return

