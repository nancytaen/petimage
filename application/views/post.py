import json
import hashlib
from datetime import datetime

from flask import Blueprint, render_template, request, session
import boto3
from botocore.client import Config

import config
from application.utility.navigation import logged_in_nav, logged_in_user

post = Blueprint('post', __name__, template_folder="templates", static_folder="static")


@post.route('/post/feed')
def feed_page():
    return render_template("post/feed.html", title="My Feed", description="Display posts",
                           nav=logged_in_nav(feed=True), user=logged_in_user())


@post.route('/post/create')
def create_post():
    return render_template("post/create_post.html", title="Create Post", description="Create post",
                           nav=logged_in_nav(create=True), user=logged_in_user())


@post.route('/sign_s3/<post_type>')
def sign_s3(post_type):

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
