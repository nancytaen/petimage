from flask import Blueprint, render_template

from application.navigation import logged_in_nav

post = Blueprint('post', __name__, template_folder="templates", static_folder="static")


@post.route('/post/feed')
def feed_page():
    return render_template("post/feed.html", title="My Feed", description="Display posts",
                           nav=logged_in_nav())
