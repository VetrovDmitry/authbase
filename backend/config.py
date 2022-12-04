from os import getenv


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    CORS_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = getenv('MAIL_DEFAULT_SENDER')
    MAIL_USE_SSL = True


class ProductionConfig(Config):
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = getenv('PROD_DB')
    CORS_ENABLED = True


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQL_DATABASE_URI = getenv('DEV_DB')
    CORS_ENABLED = True


CONFIGS = {
    "prod": ProductionConfig,
    "dev": DevelopmentConfig
}
