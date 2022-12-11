from flask import render_template, url_for, abort, flash, \
    request, redirect, current_app
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from flask_admin.helpers import is_safe_url

from app.main import bp
from app.models import Post, User, aboutPost
from app.main.forms import LoginForm


@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    for post in posts:
        sentences = post.body.split('. ')
        excerpt = ". ".join(sentences[:] if len(sentences) <= 5 else sentences[:5])
        post.body = excerpt + "." if excerpt[-1] != "." else excerpt

    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/post/<post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', title=post.title,
                           post=post)


@bp.route('/about')
def about():
    post = aboutPost.query.filter_by(title="About").first_or_404()
    return render_template('about.html', title=post.title,
                           post=post)


@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin_user = User.query.filter_by(username=form.user_name.data).first()
        if admin_user and check_password_hash(admin_user.password_hash, form.password.data):
            login_user(admin_user)
            flash(f"Welcome {admin_user.username}")
        else:
            flash('Invalid username or password')
            return render_template('login.html', form=form)

        next_url = request.args.get('next')

        if not next_url:
            next_url = url_for('admin.index')

        if not is_safe_url(next_url):
            return abort(400)

        return redirect(next_url or url_for('admin.index'))
    return render_template('login.html', form=form)


@bp.route('/admin/logout')
def logout():
    form = LoginForm()
    logout_user()
    return render_template('login.html', form=form)
