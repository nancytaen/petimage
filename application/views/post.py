import json

from flask import Blueprint, render_template, request
import boto3

from config import Config
from application.utility.navigation import logged_in_nav, logged_in_user

post = Blueprint('post', __name__, template_folder="templates", static_folder="static")


@post.route('/post/feed')
def feed_page():
    return render_template("post/feed.html", title="My Feed", description="Display posts",
                           nav=logged_in_nav(feed=True), user=logged_in_user())


@post.route('/sign_s3/')
def sign_s3():

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    print(file_name + file_type)

    s3 = boto3.client('s3', aws_access_key_id=Config.AWS_ACCESS_KEY, aws_secret_access_key=Config.AWS_SECRET_KEY)

    signature = s3.generate_presigned_post(
        Bucket=Config.S3_BUCKET,
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
        'url': 'https://%s.s3.amazonaws.com/%s' % (Config.S3_BUCKET, file_name)
    })
