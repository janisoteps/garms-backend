import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    APP_DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
