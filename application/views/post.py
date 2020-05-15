import json
import hashlib
from datetime import datetime

from flask import Blueprint, render_template, request, session, jsonify
import boto3
from botocore.client import Config

import config
from application.utility.navigation import logged_in_nav, logged_in_user
from application.form import PostCreateForm
from application.api.post import create_post_api, get_my_posts, get_post_detail, like_post_api, comment_post_api

post = Blueprint('post', __name__, template_folder="templates", static_folder="static")


@post.route('/post/feed')
def feed_page():
    my_posts = get_my_posts()
    return render_template("post/feed.html", title="My Feed", description="Display posts",
                           nav=logged_in_nav(feed=True), user=logged_in_user(), posts=my_posts)


@post.route('/post/create', methods=['GET', 'POST'])
def create_post():
    post_form = PostCreateForm(request.form)
    if request.method == 'POST':
        if post_form.validate():
            create_post_api(post_form)
    return render_template("post/create_post.html", title="Create Post", description="Create post",
                           nav=logged_in_nav(create=True), user=logged_in_user(), form=post_form)


@post.route('/post/detail/<post_id>', methods=['GET', 'POST'])
def post_page(post_id):
    post_info = get_post_detail(post_id)
    return render_template("post/post_detail.html", title="Post", description="Post detail page",
                           nav=logged_in_nav(), user=logged_in_user(), post=post_info)


@post.route('/post/like/<post_id>', methods=['GET'])
def like_post(post_id):
    """
    like a post
    :param post_id:
    :return: status 0  for success, 1 for error
    """

    if not like_post_api(post_id):
        return jsonify({'status': 1})
    return jsonify({'status': 0})


@post.route('/post/comment/<post_id>', methods=['POST'])
def comment_post(post_id):
    """
    comment on a post
    :param post_id:
    :return: status 0 for success, 1 for error
    """
    comment = request.form['comment_text']
    print(comment)
    if not comment_post_api(post_id, comment):
        return jsonify({'status': 1})
    return jsonify({'status': 0, 'comment': comment, 'username': session['username']})


@post.route('/sign_s3/<post_type>')
def sign_s3(post_type):
    """
    return s3 signature for uploading image to s3
    :param post_type:
    :return:
    """

    file_name = hashlib.sha256((request.args.get('file_name') + post_type + session['username'] +
                                str(datetime.now())).encode()).hexdigest() + ".png"
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3', aws_access_key_id=config.Config.AWS_ACCESS_KEY,
                      aws_secret_access_key=config.Config.AWS_SECRET_KEY, region_name='us-east-2',
                      config=Config(signature_version='s3v4'))

    signature = s3.generate_presigned_post(
        Bucket=config.Config.S3_BUCKET,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': signature,
        'url': 'https://%s.s3.amazonaws.com/%s' % (config.Config.S3_BUCKET, file_name)
    })
