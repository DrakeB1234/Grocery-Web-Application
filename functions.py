def login_required():
    """
        Ensure that route is only accessible to those
        that are logged into an account
    """
    if session["user_id"] == None:
        return render_template("login.html")
    else:
        return redirect("/")