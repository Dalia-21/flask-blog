from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username')
    about_me = StringField('About Me')
    submit = SubmitField('Submit')
    close = SubmitField('Close', render_kw={'data-dismiss': 'modal'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:  # add other validation criteria here
            raise ValidationError('Please use a different username.')


class EditCredentialsForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Verify Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')
    new_password2 = PasswordField('Repeat New Password', validators=[
        EqualTo('new_password')])  # if this doesn't work, do it at processing level
    submit = SubmitField('Update Credentials')
    close = SubmitField('Close', render_kw={'data-dismiss': 'modal'})

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    parent_id = HiddenField()
    submit = SubmitField('Submit')
