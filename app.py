from flask import Flask
from functools import wraps, update_wrapper
from datetime import datetime

app = Flask(__name__)

"""
    ~~~TODO~~~
    disable cache
    connect AWS database

"""

@app.route("/login")
@login_required
def login():
    return "Hello World!"