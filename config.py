import os
from dotenv import dotenv_values


basedir = os.path.abspath(os.path.dirname(__file__))
env = dotenv_values(basedir + '.env')


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'Admin'
    POSTS_PER_PAGE = 10
    BASEDIR = basedir
    if env:
        DEBUG_MODE = env['FLASK_DEBUG']
    else:
        DEBUG_MODE = False