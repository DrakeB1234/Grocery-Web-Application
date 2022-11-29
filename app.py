from flask import Flask, redirect, request, render_template

app = Flask(__name__)

"""
    ~~~TODO~~~
    disable cache
    connect AWS database

"""

# login page
@app.route("/login")
def login():
    # user posted form
    if request.method == "POST":
        return render_template("login.html")

    # user made GET request for page
    else:
        return render_template("login.html")

# home page
@app.route("/")
def home():
    return render_template("layout.html")