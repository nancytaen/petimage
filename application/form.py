from wtforms import Form, SubmitField, StringField, PasswordField, validators


class UserRegistrationForm(Form):
    email = StringField('Email Address', [
        validators.Email(message="Not a valid email address"), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(message="Please enter a password.")])
    confirm_password = PasswordField('Confirm Password', [
        validators.EqualTo(password, message="Passwords must match.")])
    submit = SubmitField('Submit')
