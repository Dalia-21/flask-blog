from flask import render_template, redirect, url_for, flash, request

import app
from app.admin import bp
from app import db
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm
from app.models import User, Post
from app.admin.forms import PostForm, PostEditForm


@bp.route('/admin', methods=['GET', 'POST'])
@bp.route('/admin/index', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.username == app.Config.ADMIN_USERNAME:
        flash('You are not allowed to access this page.')
        return redirect(url_for('main.index'))
    form = PostForm()
    if form.validate_on_submit():
        # add html formatting for newlines
        form.body.data = "<p>" + form.body.data.replace("\r\n", "</p><p>") + "</p>"

        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('admin.index'))
    posts = Post.query.all()
    return render_template('admin/index.html', title='Admin', form=form,
                           posts=posts)


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and \
            current_user.username == app.Config.ADMIN_USERNAME:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or not \
                user.username == app.Config.ADMIN_USERNAME:
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


@bp.route('/admin/post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post_to_edit = Post.query.filter_by(id=post_id).first_or_404()
    form = PostEditForm()
    if form.validate_on_submit():
        if 'back' in request.form:
            return redirect(url_for('admin.index'))
        elif 'submit' in request.form:
            post_to_edit.title = form.title.data
            post_to_edit.body = form.body.data
            db.session.commit()
            flash('Post successfully edited.')
            return redirect(url_for('admin.index'))
        elif 'delete' in request.form:
            db.session.delete(post_to_edit)
            db.session.commit()
            flash('Post successfully deleted.')
            return redirect(url_for('admin.index'))
    elif request.method == 'GET':
        form.title.data = post_to_edit.title
        form.body.data = post_to_edit.body
    return render_template('admin/edit.html', title='Edit Post',
                           form=form)


@bp.route('/admin/users', methods=['GET', 'POST'])
def users():
    user_records = User.query.all()
    if request.args.get('user_id'):
        user_to_delete = User.query.get(int(request.args.get('user_id')))
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User {} successfully deleted.'.format(user_to_delete.username))
        user_records = User.query.all()  # updating list to remove deleted user
    return render_template('admin/users.html', title='Users',
                           users=user_records)
