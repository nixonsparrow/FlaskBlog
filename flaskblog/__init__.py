from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

try:
    from .local import *  # noqa F401
except ImportError:
    pass

app = Flask(__name__)
app.config['DEBUG'] = True if os.environ.get("DEBUG") == "True" else False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "InseCuresecretKey123456!@#$%^")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")

app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT", "0"))
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True if os.environ.get("MAIL_USE_TLS") == "True" else False
app.config['MAIL_USE_SSL'] = True if os.environ.get("MAIL_USE_SSL") == "True" else False

db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = "users.login_page"
login_manager.login_message_category = "info"

from flaskblog.main.routes import main # noqa F401
from flaskblog.posts.routes import posts  # noqa F401
from flaskblog.users.routes import users  # noqa F401

app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(users)
