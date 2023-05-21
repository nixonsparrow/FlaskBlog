import os


class Config:
    DEBUG = True if os.environ.get("DEBUG") == "True" else False
    SECRET_KEY = os.environ.get("SECRET_KEY", "InseCuresecretKey123456!@#$%^")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "0"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True if os.environ.get("MAIL_USE_TLS") == "True" else False
    MAIL_USE_SSL = True if os.environ.get("MAIL_USE_SSL") == "True" else False
