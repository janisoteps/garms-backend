import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    APP_DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://garms_db_root:Superlietus4422@garms-psql1.c4b3gyurldnl.eu-west-1.rds.amazonaws.com/garmsdb1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
