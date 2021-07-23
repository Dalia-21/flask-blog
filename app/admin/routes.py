from flask import render_template, redirect, url_for, flash, abort
from werkzeug.urls import url_parse
from jinja2 import TemplateNotFound
from app.admin import bp
from flask_login import login_user, logout_user, current_user, login_required
from app.auth.forms import LoginForm, RegistrationForm
from app import db


@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.username == "admin":
        return redirect(url_for('main.index'))
    try:
        return render_template('admin/index.html')
    except TemplateNotFound:
        abort(404)


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and \
        current_user.username == 'admin':
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('auth/login.html', title='Sign In', form=form)
