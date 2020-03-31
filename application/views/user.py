from flask import Blueprint, request, render_template, redirect, url_for, flash

from application.form import UserRegistrationForm, UserLoginForm
from application.navigation import top_level_nav

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = UserRegistrationForm(request.form)
    if request.method == 'POST':
        if signup_form.validate():
            print("success")
            flash("User already exists.")
            # return redirect(url_for('user.login'))
    return render_template('user/signup.html', title="sign up",
                           description="create new account", nav=top_level_nav(), form=signup_form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    login_form = UserLoginForm(request.form)
    if request.method == "POST":
        if login_form.validate():
            print("success")
        flash("User does not exist")
    return render_template('user/login.html', title="login",
                           description="login", nav=top_level_nav(), form=login_form)
