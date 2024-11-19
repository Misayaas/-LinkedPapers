import os
# 使用时记得修改数据库url的用户名和密码（root和123456）
URL = 'mysql+pymysql://root:123456@localhost:3306'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or URL+'/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    SESSION_TYPE = 'filesystem'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or URL+'/dev_db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or URL+'/test_db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or URL+'/prod_db'