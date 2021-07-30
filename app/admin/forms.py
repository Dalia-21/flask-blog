from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('New Post', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostEditForm(PostForm):
    submit = SubmitField('Submit', render_kw={
        "onclick": "return confirm('Are you sure you want to submit these changes?')"})
    delete = SubmitField('Delete', render_kw={
        "onclick": "return confirm('Are you sure you wish to delete this post?')"})
