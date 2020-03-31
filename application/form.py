from wtforms import Form, SubmitField, StringField, PasswordField, validators


# form for user registration
class UserRegistrationForm(Form):
    email = StringField('Email Address', [
        validators.Email(message="Not a valid email address"), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(message="Please enter a password."), validators.Length(min=6)])
    confirm_password = PasswordField('Confirm Password', [
        validators.EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Create Account')


# form for user login
class UserLoginForm(Form):
    email = StringField('Email Address', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')
