import os
from flask import Flask, redirect, request, render_template, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import re
from functions import login_required, admin_access, allowed_file, save_change_time
from datetime import date, timedelta, datetime

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
    return
    


"""
    ~~~TODO~~~
    disable cache
    more safety nets for database executions
    make more efficient database executions

"""

# admin page
@app.route("/admin", methods=["GET"])
@admin_access
def admin():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    user = session.get("user")
    id = session.get("user_id")

    return render_template("admin.html", user=user[0])

# admin page mods
@app.route("/adminmod", methods=["POST"])
@admin_access
def admin_mod():
    # establish database connection
    db = mysql.connection.cursor()
    # get all user data
    db.execute('SELECT * FROM users')
    rows = db.fetchall()

    # form posted is for adding user
    if "userNameAdd" in request.form:
        inputName = request.form.get("userNameAdd")
        inputPass = request.form.get("userPassAdd")

        # input validation
        if not inputName or not inputPass:
            flash("Need name and password", "User-Error")
            return redirect("/admin")

        if not inputName.isalnum():
            flash("Use Only Letters and Numbers for Name", "User-Error")

        if not re.match("^[A-Za-z0-9$%#@!]*$",inputPass):
            flash("Only use Letters, Numbers and ($, %, #, @, !) for Password", "User-Error")
            return redirect("/admin")

        # Enuser username is not taken
        for i in rows:
            if (i["username"] == inputName):
                flash("Username Taken", "User-Error")
                return redirect("/admin")

        # insert new user into users table
        db.execute(f"INSERT INTO users (username, hash) VALUES ('{inputName}', '{generate_password_hash(inputPass)}');")
        mysql.connection.commit()

        # insert data into mealplanner for new user
        # get id of new user
        db.execute(f"SELECT user_id FROM users WHERE username = '{inputName}';")
        newID = db.fetchall()
        
        # setting 14 entries under new user in planner for later setting
        for i in range(14):
            # get weekday
            db.execute(f'''INSERT INTO mealPlanner (user_id) 
                    VALUES ({newID[0]["user_id"]});
            ''')
            mysql.connection.commit()

        flash("Added User", "Success")
        return redirect("/admin")

    if "userNameChange" in request.form:
        findName = request.form.get("userNameSelect")
        inputName = request.form.get("userNameChange")
        inputPass = request.form.get("userPassChange")

        # find user
        # Try and find users ID by inputed name
        for i in rows:
            if i["username"] == findName:
                # if match, continue code
                flash("Found User", "Success")
                findID = (i["user_id"])

                # input validation
                if not inputName and not inputPass:
                    flash("No Changes Made")
                    return redirect("/admin")

                if not inputName.isalnum() and inputName != "":
                    flash("Use Only Letters and Numbers For Name", "User-Error")
                    return redirect("/admin")

                if not re.match("^[A-Za-z0-9$%#@!]*$",inputPass) and inputPass != "":
                    flash("Only use Letters, Numbers and ($, %, #, @, !) For Password", "User-Error")
                    return redirect("/admin")

                # changes name if not empty
                if inputName != "":
                    # Ensure inputed name to be changed is unique
                    for i in rows:
                        if i["username"] == inputName:
                            # if match, continue code
                            flash("Username Taken", "User-Error")
                            findID = (i["user_id"])
                            return redirect("/admin")
                    # update username
                    db.execute(f"UPDATE users SET username = '{inputName}' WHERE user_id = {findID};")
                    mysql.connection.commit()

                # changes password if not empty
                if inputPass != "":
                    # update password
                    db.execute(f"UPDATE users SET hash = '{generate_password_hash(inputPass)}' WHERE user_id = {findID};")
                    mysql.connection.commit()

                flash("Updated User", "Success")
                return redirect("/admin")
            
        # If username cant be found, skip
        flash(f"Could not find user '{findName}'", "User-Error")
        return redirect("/admin")

    if "userNameDelete" in request.form:
        inputName = request.form.get("userNameDelete")

        # Try and find users ID by inputed name
        for i in rows:
            if i["username"] == inputName:
                # If match, continue code
                flash("Found User", "Success")
                inputName = (i["user_id"])

                # delete account
                db.execute(f"DELETE users WHERE username = {inputName};")
                mysql.connection.commit()

                flash("Deleted User '{inputName}'", "Success")
                return redirect("/admin")

            # Otherwise, user not found
            flash(f"Could Not Find User '{inputName}'", "User-Error")
            return redirect("/admin")

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
    session["user"] = None
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
    SELECT count(item) as itemCount, count(title) as listCount
    FROM listData as ld
    JOIN listTitles as lt ON lt.id = ld.title_id
    WHERE lt.user_id = {id} 
    ''')
    grocery += db.fetchall()

    # getting users current meal plan (based on current date)
    now = date.today()
    db.execute(f'''
    SELECT meal
    FROM mealPlanner 
    WHERE user_id = {id} AND
    date = '{now}'
    ''')
    curMeal = db.fetchall()

    # if no meal is found
    if curMeal == ():
        curMeal = "Nothing Planned!"
    else:
        curMeal = curMeal[0]["meal"]

    # setting tuple
    curMeal = ({"month" : now.strftime("%B"), "day" : now.strftime("%d"), "meal" : curMeal})

    recipe = []
    # select recipes stats 
    db.execute(f'''
    SELECT count(recipe_name) as count
    FROM recipes
    WHERE user_id = {id} 
    ''')
    fetch = db.fetchall()
    recipe.append(fetch[0]["count"])

    # select saved recipes stats 
    db.execute(f'''
    SELECT count(recipe_id) as count
    FROM saverecipes
    WHERE user_id = {id} 
    ''')
    fetch = db.fetchall()
    recipe.append(fetch[0]["count"])

    # select saved recipes stats 
    db.execute(f'''
    SELECT saved_amount
    FROM recipes
    WHERE user_id = {id} 
    ''')
    fetch = db.fetchall()

    # adds total amount of saves between all recipes
    total = 0
    for i in fetch:
        total += i["saved_amount"]

    recipe.append(total)

    return render_template("home.html", user=user[0], url=request.path, grocery=grocery, grocerytime=session.get("grocery_time"), curMeal=curMeal, recipe=recipe)

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
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
            # get new user info to get new avatar path
            user_info(id)
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
                
            if  len(inputName) < 3 or len(inputName) > 20:
                flash("Only use between 3 and 20 characters", "User-Error")
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
    SELECT id, date, DAY(date) as day, weekday, meal
    FROM mealPlanner 
    WHERE user_id = {id} 
    ORDER BY date ASC
    ''')
    mealplan = db.fetchall()

    if mealplan == ():
        flash("Error Loading Meal Planner, Contact Admin", "Server-Error")
        return redirect("/")

    # get current month and year
    try: 
        month = mealplan[7]["date"].strftime("%B")
    except:
        month = "unset"

    try: 
        year = mealplan[7]["date"].strftime("%Y")
    except:
        year = "unset"

    # getting users saved recipes
    db.execute(f'''
    SELECT sr.*, r.recipe_name
    FROM saverecipes as sr
    JOIN recipes as r ON r.recipe_id = sr.recipe_id
    WHERE sr.user_id = {id}
    ''')
    saved = db.fetchall()

    # getting users created recipes
    db.execute(f'''
    SELECT *
    FROM recipes
    WHERE user_id = {id}
    ''')
    myrecipes = db.fetchall()

    return render_template("mealplanner.html", user=user[0], url=request.path, mealplan=mealplan, month=month, year=year, saved=saved, myrecipes=myrecipes)

# mealplanner mod page
@app.route("/mealplannermod", methods=["POST"])
@login_required
def mealplanmod():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    # new planner is being requested
    if "mealStartDate" in request.form:
        start = request.form.get("mealStartDate")
        weekAmnt = request.form.get("mealWeekAmnt")

        # input validation
        if not start or not weekAmnt:
            flash("Fill All Required Inputs", "User-Error")
            return redirect("/mealplanner")
        
        try:
            weekAmnt = int(weekAmnt)
        except:
            flash("Week needs to be a number", "User-Error")
            return redirect("/mealplanner")

        if not weekAmnt == 7 and not weekAmnt == 14:
            flash("Week needs to be between 7 and 14 days", "User-Error")
            return redirect("/mealplanner")

        # clearing db
        db.execute(f'''
                UPDATE mealPlanner 
                SET date = NULL, weekday = NULL, meal = "Unset"
                WHERE user_id = {id};
        ''')
        mysql.connection.commit()

        # setting 14 entries under new user in planner for later setting
        now = datetime.strptime(start, '%Y-%m-%d').date()
        # getting id of first mealplanner by user
        db.execute(f'SELECT id FROM mealPlanner WHERE user_id = {id} LIMIT 1;')
        planID = db.fetchall()
        planID = planID[0]["id"]

        for i in range(weekAmnt):
            # get weekday
            weekday = now.strftime("%a").upper()
            
            # updating db
            db.execute(f'''
                    UPDATE mealPlanner 
                    SET date = '{now}', weekday = '{weekday}'
                    WHERE user_id = {id} AND
                    id = {planID};
            ''')
            mysql.connection.commit()

            # increment day and id
            now = now + timedelta(days = 1)
            planID += 1
        
        # flash message of success
        flash("Added New Week to Planner", "Success")
        return redirect("/mealplanner")

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

# recipes home page
@app.route("/recipes", methods=["GET"])
@login_required
def recipes():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    user = session.get("user")
    id = session.get("user_id")

    # if user is searching for recipe
    if request.args.get("search"):
        type = request.args.get("searchType")
        
        if not type or type not in ["recipe_name", "category", "course"]:
            flash("Must provide proper input", "User-Error")
            return redirect('/recipes')

        # getting randomized recipes
        db.execute(f'''
        SELECT *
        FROM recipes 
        WHERE {type} LIKE '%{request.args.get("search")}%'
        ORDER BY RAND()
        ''')
        recipelist = db.fetchall()
    else:
        # getting randomized recipes
        db.execute(f'''
        SELECT *
        FROM recipes 
        ORDER BY RAND()
        LIMIT 12
        ''')
        recipelist = db.fetchall()

    # getting saved recipes
    db.execute(f'''
    SELECT recipe_id
    FROM saverecipes 
    WHERE user_id = {id}
    ''')
    savelist = db.fetchall()
    
    # converting array to just id numbers
    temp = []
    for i in savelist:
        temp.append(i['recipe_id'])
    savelist = temp

    return render_template("recipes.html", user=user[0], url=request.path, recipelist=recipelist, savelist=savelist)

# recipes view page
@app.route("/recipesview", methods=["GET"])
def recipes_view():
    # establish database connection
    db = mysql.connection.cursor()

    # try getting an user id
    try: 
        id = session["user_id"]
    except:
        id = None

    # if no id is set (user not signed in)
    if(id == None):
        id = 0
        user = ({"user_id" : 0, "username" : "Guest"},)
    else:
        user = session.get("user")

    recipeName = request.args["recipe"]
    recipeID = request.args["id"]

    # getting specified recipe
    db.execute(f'''
    SELECT recipes.*, username
    FROM recipes
    JOIN users ON users.user_id = recipes.user_id
    WHERE recipe_id = {recipeID} AND
    recipe_name = '{recipeName}';
    ''')
    recipelist = db.fetchall()

    # getting instructions based off of recipe ID
    db.execute(f'''
    SELECT instructions_name
    FROM instructions
    WHERE recipe_id = {recipeID}
    ''')
    instructions = db.fetchall()

    # getting ingredients based off of recipe ID
    db.execute(f'''
    SELECT ingredient_name, ingredient_measure
    FROM ingredients
    WHERE recipe_id = {recipeID}
    ''')
    ingredients = db.fetchall()

    # getting saved recipes if user is signed in
    if id != None:
        db.execute(f'''
        SELECT recipe_id
        FROM saverecipes 
        WHERE user_id = {id} AND
        recipe_id = {recipeID}
        ''')
        saved = db.fetchall()

        # checking if recipe was saved
        if saved != ():
            saved = True
        else:
            saved = False
    else:
        saved = False

    url = f"http://192.168.0.199:5000/recipesview?recipe={recipeName}&id={recipeID}"
    print(url)
    

    return render_template("recipesview.html", user=user[0], url=url, recipe=recipelist[0], instructions=instructions, ingredients=ingredients, saved=saved)

# recipes user page
@app.route("/recipesuser", methods=["GET"])
@login_required
def recipes_user():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]
    # get user details
    user = session.get("user")

    # getting users recipes
    db.execute(f'''
        SELECT recipes.*, username
        FROM recipes
        JOIN users ON users.user_id = recipes.user_id
        WHERE recipes.user_id = {id};
    ''')
    recipelist = db.fetchall()

    # getting instructions based off of recipe ID
    db.execute(f'''
    SELECT instructions.*, recipes.recipe_id
    FROM instructions
    JOIN recipes ON instructions.recipe_id = recipes.recipe_id
    WHERE recipes.user_id = {id};
    ''')
    instructions = db.fetchall()

    # getting instructions based off of recipe ID
    db.execute(f'''
    SELECT ingredients.*, recipes.recipe_id
    FROM ingredients
    JOIN recipes ON ingredients.recipe_id = recipes.recipe_id
    WHERE recipes.user_id = {id};
    ''')
    ingredients = db.fetchall()

    return render_template("recipesuser.html", user=user[0], url=request.path, recipe=recipelist, instructions=instructions, ingredients=ingredients)


# recipes view page
@app.route("/recipesmod", methods=["POST"])
@login_required
def recipes_mod():
    # establish database connection
    db = mysql.connection.cursor()
    # get user details
    id = session.get("user_id")

    # if request is to save recipe
    if "recipeSave" in request.form:
        recipeID = request.form.get('recipeSave')
        if not recipeID or not recipeID.isnumeric():
            flash("Invalid input", "User-Error")
            return redirect("/recipes")

        # Executing sql query
        db.execute(f'''
            INSERT INTO saverecipes (user_id, recipe_id)
            VALUES ({id}, {recipeID})
        ''')
        mysql.connection.commit()

        # adding saved amount
        db.execute(f'''
            UPDATE recipes
            SET saved_amount = saved_amount + 1
            WHERE recipe_id = {recipeID}
        ''')
        mysql.connection.commit()

        flash("Saved Recipe", "Success")
        return redirect("/recipes")
    
    # if request is to unsave recipe
    if "recipeUnsave" in request.form:
        recipeID = request.form.get('recipeUnsave')
        if not recipeID or not recipeID.isnumeric():
            flash("Invalid input", "User-Error")
            return redirect("/recipes")

        # Executing sql query
        db.execute(f'''
            DELETE 
            FROM saverecipes
            WHERE recipe_id = {recipeID} AND
            user_id = {id}
        ''')
        mysql.connection.commit()

        # adding saved amount
        db.execute(f'''
            UPDATE recipes
            SET saved_amount = saved_amount - 1
            WHERE recipe_id = {recipeID}
        ''')
        mysql.connection.commit()

        flash("Unsaved Recipe", "Success")
        return redirect("/recipes")

    # if request is to add recipe
    if "recipeAddTitle" in request.form:
        title = request.form.get("recipeAddTitle")
        outerlink = request.form.get('recipeOuterLink')
        course = request.form.get('recipeAddCourse')
        category = request.form.get('recipeAddCategory')
        description = request.form.get('recipeAddDescription')
        file = request.files['avatarFile']
        ingredients = request.form.getlist("recipeIngredients")
        measure = request.form.getlist("recipeMeasure")
        instructions = request.form.getlist("recipeInstructions")
        
        # input validation
        if not title or not course or not category or not description or not ingredients[0] or not measure[0] or not instructions[0]:
            flash("Missing Required Input", "User-Error")
            return redirect("/recipes")

        if not re.match("^[a-zA-Z][a-zA-Z ]*$", title) or not re.match("^[a-zA-Z][a-zA-Z ]*$", category):
            flash("Only use letters and spaces for title and category", "User-Error")
            return redirect("/recipes")

        if outerlink != "":
            if not re.match("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", outerlink):
                flash("Invalid Format For Reference Link", "User-Error")
                return redirect("/recipes")

        if course not in ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]:
            flash("Only use 'Breakfast', 'Lunch', 'Dinner', 'Snack', or 'Dessert' for course", "User-Error")
            return redirect("/recipes")

        if not re.match("^[a-zA-Z0-9][a-zA-Z0-9!?.,' ]*$", description):
            flash("Only use letters, numbers, spaces, and ! ? . , ' for description", "User-Error")
            return redirect("/recipes")

        # check for empty items in ingredients and non-valid input, if there is /error
        for i in ingredients:
            if not i or not re.match("^[a-zA-Z][a-zA-Z ]*$", i):
                flash("Only use letters and spaces for ingredients", "User-Error")
                return redirect("/recipes")

        # check for empty items in measure and non-valid input, if there is /error
        for i in measure:
            if not i or not re.match("^[a-zA-Z0-9][a-zA-Z0-9\/\- ]*$", i):
                flash("Only use letters, numbers, spaces, and - / for amounts", "User-Error")
                return redirect("/recipes")

        # check for empty items in measure and non-valid input, if there is /error
        for i in instructions:
            if not i or not re.match("^[a-zA-Z0-9][a-zA-Z0-9!\-,./()' ]*$", i):
                flash("Only use letters, numbers, spaces, and ! . , ' / - ( ) for instructions", "User-Error")
                return redirect("/recipes")
        
        # Executing sql query
        db.execute(f'''
            INSERT INTO recipes 
            (user_id, course, category, recipe_name, description, image_path, outer_link, saved_amount)
            VALUES ({id}, "{course}", "{category}", "{title}", "{description}", "/static/images/recipes/graphic-recipe.svg", "{outerlink}", 0)   
        ''')
        mysql.connection.commit()

        # get last recipe id (one just inserted)
        db.execute('SELECT recipe_id FROM recipes ORDER BY recipe_id DESC LIMIT 1;')
        recipeID = db.fetchall()

        # if user selects image
        if file.filename != '':
            app.config['UPLOAD_FOLDER'] = 'static/images/recipes'
            # format naming of filename
            file.filename = f"recipeCoverImage{recipeID[0]['recipe_id']}.jpg"
            
            # allowed file checks for allowed extensions
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pathVar = app.config['UPLOAD_FOLDER'] + "/" + file.filename
            # updating recipe with image var
            db.execute(f'UPDATE recipes SET image_path = "/{pathVar}" WHERE recipe_id = {recipeID[0]["recipe_id"]}')
            mysql.connection.commit()

        # Executing sql query
        for i in range(len(ingredients)):
            db.execute(f'''
                INSERT INTO ingredients 
                (recipe_id, ingredient_name, ingredient_measure)
                VALUES ({recipeID[0]["recipe_id"]}, "{ingredients[i]}", "{measure[i]}")
            ''')
            mysql.connection.commit()

        # Executing sql query
        for i in range(len(instructions)):
            db.execute(f'''
                INSERT INTO instructions 
                (recipe_id, instructions_name)
                VALUES ({recipeID[0]["recipe_id"]}, "{instructions[i]}")
            ''')
            mysql.connection.commit()

        return redirect("/recipes")

    # if request is to edit recipe
    if "recipeDelete" in request.form:
        recipeID = request.form.get("recipeDelete")

        if not recipeID or not recipeID.isnumeric():
            flash("Invalid input", "User-Error")
            return redirect("/recipes")
        
        # Executing sql query
        db.execute(f'''
            DELETE inst
            FROM instructions as inst
            JOIN recipes as r ON inst.recipe_id = r.recipe_id
            WHERE inst.recipe_id = {recipeID} AND 
            r.user_id = {id}
        ''')
        mysql.connection.commit()

        db.execute(f'''
            DELETE ingre
            FROM ingredients as ingre
            JOIN recipes as r ON ingre.recipe_id = r.recipe_id
            WHERE ingre.recipe_id = {recipeID} AND 
            r.user_id = {id}
        ''')
        mysql.connection.commit()

        db.execute(f'''
            DELETE
            FROM recipes
            WHERE recipe_id = {recipeID} AND 
            user_id = {id}
        ''')
        mysql.connection.commit()

        flash("Deleted Recipe", "Success")
        return redirect("/recipes")

    # if request is to edit recipe
    if "recipeEditTitle" in request.form:
        recipeID = request.form.get("recipeEditID")
        title = request.form.get("recipeEditTitle")
        outerlink = request.form.get('recipeEditLink')
        course = request.form.get('recipeEditCourse')
        category = request.form.get('recipeEditCategory')
        description = request.form.get('recipeEditDescription')
        file = request.files['avatarFile']
        ingredients = request.form.getlist('recipeIngredients')
        instructions = request.form.getlist('recipeInstructions')

        # check for valid ID
        if not recipeID or not re.match("^[0-9]*$", recipeID):
            flash("Invalid input used", "User-Error")
            return redirect("/recipesuser")

        # checking if any edits were submitted
        if title:
            if not re.match("^[a-zA-Z][a-zA-Z ]*$", title):
                flash("Only use letters and spaces for Title", "User-Error")
            else:
                # Executing sql query
                db.execute(f'''
                    UPDATE recipes
                    SET recipe_name = '{title}'
                    WHERE recipe_id = {recipeID} AND 
                    user_id = {id}
                ''')
                mysql.connection.commit()
                flash("Changed Recipe Name", "Success")

        if outerlink:
            if not re.match("(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", outerlink):
                flash("Invalid URL", "User-Error")
            else:
                # Executing sql query
                db.execute(f'''
                    UPDATE recipes
                    SET outer_link = '{outerlink}'
                    WHERE recipe_id = {recipeID} AND 
                    user_id = {id}
                ''')
                mysql.connection.commit()
                flash("Changed Link", "Success")

        if course:
            if course not in ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]:
                flash("Only use 'Breakfast', 'Lunch', 'Dinner', 'Snack', or 'Dessert' for course", "User-Error")
            else:
                # Executing sql query
                db.execute(f'''
                    UPDATE recipes
                    SET course = '{course}'
                    WHERE recipe_id = {recipeID} AND 
                    user_id = {id}
                ''')
                mysql.connection.commit()
                flash("Changed Course", "Success")

        if category:
            if not re.match("^[a-zA-Z][a-zA-Z ]*$", category):
                flash("Only use letters and spaces for Category", "User-Error")
            else:
                # Executing sql query
                db.execute(f'''
                    UPDATE recipes
                    SET category = '{category}'
                    WHERE recipe_id = {recipeID} AND 
                    user_id = {id}
                ''')
                mysql.connection.commit()
                flash("Changed Category", "Success")

        if description:
            if not re.match("^[a-zA-Z0-9][a-zA-Z0-9!?.,' ]*$", description):
                flash("Only use letters, numbers, spaces, and ! ? . , ' for Description", "User-Error")
            else:
                # Executing sql query
                db.execute(f'''
                    UPDATE recipes
                    SET description = '{description}'
                    WHERE recipe_id = {recipeID} AND 
                    user_id = {id}
                ''')
                mysql.connection.commit()
                flash("Changed Description", "Success")

        # if user selects image
        if file.filename != '':
            app.config['UPLOAD_FOLDER'] = 'static/images/recipes'
            # format naming of filename
            file.filename = f"recipeCoverImage{recipeID}.jpg"
            
            # allowed file checks for allowed extensions
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            pathVar = app.config['UPLOAD_FOLDER'] + "/" + file.filename
            # if file is successful, change file path in recipe
            db.execute(f"UPDATE recipes SET image_path = '{pathVar}' WHERE user_id = {id} AND recipe_id = {recipeID}")

            mysql.connection.commit()
            flash("Changed Image", "Success")

        # if there is one value that is not '' then run code
        if not all(i == '' for i in ingredients):
            # get all ids for instructions if input is provided
            ingredientsID = request.form.getlist('recipeIngredientsID')
            for idx, x in enumerate(ingredients):
                if x != '':
                    print(x)
                    print(ingredientsID[idx])
            flash('Changed Ingredients', 'Success')

        # if there is one value that is not '' then run code
        if not all(i == '' for i in instructions):
            # get all ids for instructions if input is provided
            instructionsID = request.form.getlist('recipeInstructionsID')
            for idx, x in enumerate(instructions):
                if x != '' and re.match("^[a-zA-Z0-9][a-zA-Z0-9!\-,./()' ]*$", x) and instructionsID[idx].isnumeric():
                    # Executing sql query
                    db.execute(f'''
                        UPDATE instructions
                        JOIN recipes ON instructions.recipe_id = recipes.recipe_id
                        SET instructions_name = '{x}'
                        WHERE recipes.recipe_id = {recipeID} AND 
                        instructions_id = {instructionsID[idx]} AND
                        user_id = {id}
                    ''')
                    mysql.connection.commit()
            flash('Changed Instructions', 'Success')

        return redirect("/recipesuser")
    return redirect("/recipesuser")

# recipes user page
@app.route("/recipesaved", methods=["GET", "POST"])
@login_required
def recipes_saved():
    # establish database connection
    db = mysql.connection.cursor()
    id = session["user_id"]

    if request.method == "POST":
        return redirect("/recipesaved") 
    else:
        # get user details
        user = session.get("user")

        # getting users saved recipes
        db.execute(f'''
            SELECT recipes.*
            FROM recipes
            JOIN saverecipes ON saverecipes.recipe_id = recipes.recipe_id
            WHERE recipes.recipe_id = saverecipes.recipe_id AND
            saverecipes.user_id = {id};
        ''')
        recipelist = db.fetchall()

        print(recipelist)

        return render_template("recipesaved.html", user=user[0], recipe=recipelist)

@app.errorhandler(404)
def page_not_found(e):
    flash("Page Not Found", "Server-Error")
    return redirect('/')

@app.errorhandler(405)
def page_not_found(e):
    flash("Method Not Allowed", "Server-Error")
    return redirect('/')

@app.errorhandler(500)
def internal_error(e):
    flash("Internal Error, Contact Admin", "Server-Error")
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)