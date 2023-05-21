from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login_page"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)

    from flaskblog.main.routes import main # noqa F401
    from flaskblog.posts.routes import posts  # noqa F401
    from flaskblog.users.routes import users  # noqa F401

    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app
