from flask import Blueprint, request, render_template, redirect, url_for, flash, session

from application.form import UserRegistrationForm, UserLoginForm
from application.navigation import top_level_nav
from application.api.user import signup_api, login_api
from application.message import UserMessage
from application.decorators import login_required

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = UserRegistrationForm(request.form)
    if request.method == 'POST':
        if signup_form.validate():
            message = signup_api(signup_form)
            if message != UserMessage.SIGNUP_SUCCESS:
                flash(message)
            else:
                flash("Please verify the link sent to your email before proceeding.")
                return redirect(url_for('user.login'))
    return render_template('user/signup.html', title="Create Account",
                           description="create new account", nav=top_level_nav(signup=True), form=signup_form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    login_form = UserLoginForm(request.form)
    if request.method == "POST":
        if login_form.validate():
            message = login_api(login_form)
            if message != UserMessage.LOGIN_SUCCESS:
                flash(message)
            else:
                flash("Success")
    return render_template('user/login.html', title="Login",
                           description="Login", nav=top_level_nav(login=True), form=login_form)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    return redirect(url_for('top_page'))


@user.route('/api/email_verif/<token>', methods=['GET'])
def verify_email_token(token):
    flash("Email has been confirmed!")
    return redirect(url_for('user.login'))
