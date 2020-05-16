from flask import Flask, render_template, session, redirect, url_for
from flask_cors import CORS

from config import Config
from application.model.model import init_db
from application.views import user, post
from application.utility.navigation import top_level_nav


def create_app():
    # instantiate the app
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # register blueprints
    with app.app_context():
        app.register_blueprint(user.user)
        app.register_blueprint(post.post)

    @app.route('/')
    @app.route('/top')
    def top_page():
        if session.get('logged_in'):
            return redirect(url_for('post.feed_page', username=session['username']))
        return render_template("top.html",
                               title="top", description="this is top",
                               nav=top_level_nav())

    # instantiate db connection
    init_db()

    return app
