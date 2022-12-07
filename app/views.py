from flask_login.utils import current_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose


class MyModelView(ModelView):
    @expose('/admin')
    @login_required
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated()
