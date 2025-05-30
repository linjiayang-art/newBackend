import os
import sys

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#SQLite URI compatible
WIN=sys.platform.startswith('win')
if WIN:
    prefix='sqlite:///'
else:
    prefix='sqlite:////'

    
class BaseConfig:
    #APP KEY
    SECRET_KEY=os.getenv('SECRET_KEY','\x1d\r\xc9\x8b(B\x98\x8c\xf9\x0c\na')
    #
    DEBUG_TB_INTERCEPT_REDIRECTS=False
    DEBUG_TB_ENABLED=False
    #SQL ALCHEMY
    SQLALCHEMY_RECORD_QUERIES=True
    BACKEND_SLOW_QUERY_THRESHOLD=0.001
    #database
    
    SQLALCHEMY_DATABASE_URI="mssql+pymssql://sa:123456@172.16.3.249/backend?charset=utf8"
 
    JSON_AS_ASCII=False
    # SQLALCHEMY_BINDS={ 'sicore':'mysql://it:it_123456@172.16.3.226/sicore',
    #                    }

    #MAIL
    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAID_DEFAULT_SENDER=f'BackEnd <{MAIL_USERNAME}>'

    BACKEND_ADMIN_EMAIL=os.getenv('BACKEND_ADMIN_MAIL')
    


    #QUERT PAGE
    BACKEND_POST_PER_PAGE=10
    BACKEND_MANAGE_POST_PER_PAGE=15
    BACKEND_COMMENT_PER_PAGE=15
    BACKEND_SLOW_QUERY_THRESHOLD=0.1
    #FILE
    UPLOAD_PATH=os.path.join(basedir,'uploads')
    LOG_DIR=os.path.join(basedir, 'logs')
    FILE_DIR=os.path.join(basedir,'modelfile')
    CACHEFILE_DIR=os.path.join(basedir,'cachefile')
   

    MAX_CONTENT_LENGTH=20*1024*1024
    BACKEND_ALLOWED_IMAGE_EXTENSIONS=['png','jpg','jpeg','gif']


class DevelopmentConfig(BaseConfig):
    
    #SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    pass

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

config={
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }