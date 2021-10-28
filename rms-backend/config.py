import configparser
import os
import uuid

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SECURITY_PASSWORD_SALT = uuid.uuid4().hex


class RmsConfig(Config):
    config = configparser.RawConfigParser()
    config.read(BASE_DIR + '/rms.ini')

    # for app setting
    SQLALCHEMY_DATABASE_URI = config.get('APP', 'SQLALCHEMY_DATABASE_URI')
    WX_APP_ID = config.get('APP', 'WX_APP_ID')
    WX_APP_SECRET = config.get('APP', 'WX_APP_SECRET')
