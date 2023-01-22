from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    log_file = app.config['BASEDIR'] + "/logs/error.log"
    log_format = f'%(asctime)s %(levelname)s %(name)s : %(message)s'
    if app.config['DEBUG_MODE']:
        log_level = logging.DEBUG
    else:
        log_level = logging.ERROR

    logging.basicConfig(filename=log_file, level=log_level, format=log_format)

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    from app.views import admin
    admin.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    bootstrap.init_app(app)

    return app
