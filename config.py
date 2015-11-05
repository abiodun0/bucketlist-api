import os
from datetime import timedelta

class BaseConfig:
    """ Defines base configurations that are common across all deploys.
    """
    
    SECRET_KEY = os.environ.get('BUCKETLIST_SECRET_KEY') or 'NoSecretKey'
    DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100
    
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True



        
class DevelopmentConfig(BaseConfig):
    """ Defines configurations for development
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"

class TestingConfig(BaseConfig):
    """ Defines configurations for testing
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://bucketlist_user:pass_12@127.0.0.1/bucketlist"
   


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