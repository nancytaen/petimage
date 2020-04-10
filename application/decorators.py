from functools import wraps

from flask import session, flash, redirect, url_for


def login_required(f):
    """
    decorator for login required function
    redirects to login page if not logged in
    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        print(session)
        if session['logged_in'] is True:
            return f(*args, **kwargs)
        else:
            flash("Login is required.")
            return redirect(url_for('user.login'))
    return wrap
