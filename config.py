import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """ Sets base configurations that are common across all deploys.
    """
    
    SECRET_KEY = os.environ.get('BUCKETLIST_SECRET_KEY') or 'NoSecretKey'
    DEFAULT_PER_PAGE = 2
    MAX_PER_PAGE = 1000
    TOKEN_EXPIRE = 6000
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_COVERAGE = "ieoajifeoajefoa"

        
class DevelopmentConfig(BaseConfig):
    """ Sets configurations for development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"

class TestingConfig(BaseConfig):
    """ Sets configurations for testing"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('BUCKETLIST_TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bucketlist-test.sqlite')
   


class ProductionConfig(BaseConfig):
    """ Sets configurations for production"""
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"
    


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}