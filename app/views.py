from flask_login.utils import current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for
from app.models import User, Post, aboutPost
from flask_admin import AdminIndexView, expose
from flask_admin.base import MenuLink
from flask_admin import Admin
from app import login_manager
from flask import request
from app import db


class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            if current_user.admin:
                return self.render('/admin/index.html')
        return self.render(url_for('main.login'))

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login', next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.login'))


admin = Admin(index_view=SecureAdminIndexView())
admin.add_view(SecureModelView(Post, db.session, name='Posts'))
admin.add_view(SecureModelView(aboutPost, db.session, name='About Posts'))

logout_link = MenuLink(name='Logout', url='/admin/logout')
admin.add_link(logout_link)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
