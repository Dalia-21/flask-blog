import jinja2
from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config
from config import env_override
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()

jinja2.filters.FILTERS['env_override'] = env_override # was this a hack?

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db.init_app(app)
    migrate.init_app(app, db)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    bootstrap.init_app(app)

    return app

from app import models