# coding: utf-8

import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DATABASE_URI = os.environ.get('DATABASE_URL', None)
# if not DATABASE_URI:
#     raise Exception('Please, export DATABASE_URL variable')


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False
    LOGFILE = './logs/Production.log'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    USE_RELOADER=False
    LOGFILE = 'botService/logs/Development.log'


class TestingConfig(Config):
    TESTING = True

