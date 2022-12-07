"""WARNING: This is a file for temporary python code, while I rearrange file structure."""

from flask_admin import helpers as admin_helpers
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, \
    login_required, current_user
from flask_admin.contrib.sqla import ModelView


class SecureModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser'))

    def _handle_view(self, name, **kwargs):
        """
        Override builtin handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                Flask.abort(403)
            else:
                # login
                return Flask.redirect(Flask.url_for('security.login', next=Flask.request.url))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

from app.models import Post

admin.add_view(SecureModelView(Post, db.session))
security = Security(app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=Flask.url_for
    )
