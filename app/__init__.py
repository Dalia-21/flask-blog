from flask import Flask
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    bootstrap.init_app(app)

    return app
