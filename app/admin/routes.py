from flask import render_template, redirect, url_for, flash
from app.admin import bp
from app import db
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm
from app.models import User, Post
from app.admin.forms import PostForm


@bp.route('/admin', methods=['GET', 'POST'])
@bp.route('/admin/index', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.username == "admin":
        flash('You are not allowed to access this page.')
        return redirect(url_for('main.index'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('admin.admin'))
    posts = Post.query.all()
    return render_template('admin/index.html', title='Admin', form=form,
                           posts=posts)


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and \
            current_user.username == 'admin':
        return redirect(url_for('admin.admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or not \
                user.username == "admin":
            flash("Invalid username or password.")
            return redirect(url_for('admin.login'))  # behaviour could be improved
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.login'))
    # currently just reusing standard login page
    return render_template('auth/login.html', title='Sign In', form=form)


"""current behaviour is not as expected: admin when forced to login
is redirected to standard index page"""


@bp.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


"""required routes: post submission, post editing, users, user view, post view"""
