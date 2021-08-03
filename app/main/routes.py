from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from app.models import Post, User
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, EditCredentialsForm


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.all()
    for post in posts:
        sentences = post.body.split('. ')
        excerpt = ". ".join(sentences[:] if len(sentences) <= 3 else sentences[:3])
        post.body = excerpt + "." if excerpt[-1] != "." else excerpt
    return render_template('index.html', title='Home', posts=posts)


@bp.route('/post/<post_id>')
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', title=post.title,
                           post=post)


@bp.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required  # also need to ensure user matches logged in user
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    profile_form = EditProfileForm()
    credentials_form = EditCredentialsForm()
    if profile_form.validate_on_submit():
        if profile_form.username.data:
            user.username = profile_form.username.data
        if profile_form.about_me.data:
            user.about_me = profile_form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Profile data successfully updated.')
    elif credentials_form.validate_on_submit():
        if not user.check_password(credentials_form.password.data):
            flash('Incorrect password.')
            return redirect(url_for('main.profile', user_id=current_user.id))
        user.email = credentials_form.email.data
        if credentials_form.new_password:
            user.set_password(credentials_form.new_password.data)
        db.session.add(user)
        db.session.commit()
        flash('Credentials successfully updated.')
    return render_template('profile.html', title=user.username,
                           user=user, profile_form=profile_form,
                           credentials_form=credentials_form)
