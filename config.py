import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    pass

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

