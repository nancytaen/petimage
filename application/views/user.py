from flask import Blueprint, request, render_template

from application.navigation import top_level_nav

user = Blueprint('user', __name__, template_folder='templates', static_folder='static')


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('user/signup.html', title="sign up",
                               description="create new account", nav=top_level_nav())
