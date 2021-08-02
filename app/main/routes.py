from flask import render_template
from flask_login import login_required

from app.main import bp
from app.models import Post, User


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


@bp.route('/user/<user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('profile.html', title=user.username,
                           user=user)