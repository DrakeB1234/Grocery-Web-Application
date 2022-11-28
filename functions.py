def login_required():
    """
        Ensure that route is only accessible to those
        that are logged into an account
    """
    if session["user_id"] = None:
        return False
    return True