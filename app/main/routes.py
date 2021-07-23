from flask import render_template
from app.main import bp
from app.models import Post


@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)
