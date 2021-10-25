import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class Config:
    DEBUG = False

    JWT_ERROR_MESSAGE_KEY = 'message'

    UPLOADED_IMAGES_DEST = 'static/images'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super-secret-key'

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)


class StagingConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')