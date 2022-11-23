from flask import render_template, redirect, url_for, flash, request

from app.admin import bp
from app import db
from app.models import Post
from app.admin.forms import PostForm, PostEditForm

# NO AUTHENTICATION REQUIRED; FOR DEV PURPOSES ONLY!!!
@bp.route('/admin', methods=['GET', 'POST'])
@bp.route('/admin/index', methods=['GET', 'POST'])
def index():
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

