from flask import Flask, redirect, request, render_template, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

"""
    ~~~TODO~~~
    disable cache
    connect AWS database

"""

# login page
@app.route("/login", methods=["POST", "GET"])
def login():
    # user posted form
    if request.method == "POST":
        flash(request.form.get("userName"))
        return render_template("login.html")

    # user made GET request for page
    else:
        return render_template("login.html")

# home page
@app.route("/")
def home():
    return render_template("layout.html")