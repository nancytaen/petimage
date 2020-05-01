from wtforms import Form, SubmitField, StringField, PasswordField, FileField, validators


# form for user registration
class UserRegistrationForm(Form):
    email = StringField("email", description="Email Address", validators=[
        validators.Email(message="Not a valid email address"), validators.DataRequired()])
    password = PasswordField('password', description="Password", validators=[
        validators.DataRequired(message="Please enter a password."), validators.Length(min=6)])
    confirm_password = PasswordField('confirm_password', description='Confirm Password', validators=[
        validators.EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Create Account')


# form for user login
class UserLoginForm(Form):
    email = StringField('Email Address', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')


class UserAccountForm(Form):
    email = StringField('email', description="Email", validators=[validators.DataRequired()])
    username = StringField('username', description="Username", validators=[validators.DataRequired()])
    profile_img_url = StringField('profile_img_url')


class PostCreateForm(Form):
    post_title = StringField('Title')
    post_img_url = StringField('post_img_url', validators=[validators.DataRequired()])
    post_body = StringField('Body')
