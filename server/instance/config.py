import os


class Config(object):
    """Base config"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = '{}/horethNetDev'.format(os.getenv('DATABASE_URI'))


class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True


class TestingConfig(Config):
    """Testing config"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = '{}/horethNetTest'.format(os.getenv('DATABASE_URI'))
    DEBUG = True

class ProductionConfig(Config):
    """Production config"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = '{}/horethNet'.format(os.getenv('DATABASE_URI'))


app_config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig
}