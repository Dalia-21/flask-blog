from flask import render_template, abort
from app.main import bp
from jinja2 import TemplateNotFound


@bp.route('/')
@bp.route('/index')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
