from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('New Post', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostEditForm(PostForm):
    delete = SubmitField('Delete')
