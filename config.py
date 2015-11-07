import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """ Defines base configurations that are common across all deploys.
    """
    
    SECRET_KEY = os.environ.get('BUCKETLIST_SECRET_KEY') or 'NoSecretKey'
    #ATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_PER_PAGE = 2
    MAX_PER_PAGE = 1000
    TOKEN_EXPIRE = 6000
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_COVERAGE = "ieoajifeoajefoa"
    #SERVER_NAME = "http://127.0.0.1:5000/"

        
class DevelopmentConfig(BaseConfig):
    """ Defines configurations for development
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"

class TestingConfig(BaseConfig):
    """ Defines configurations for testing
    """
    TESTING = True
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist_test"
    SQLALCHEMY_DATABASE_URI = os.environ.get('BUCKETLIST_TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bucketlist-test.sqlite')
   


class ProductionConfig(BaseConfig):
    """ Defines configurations for production
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"
    


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}