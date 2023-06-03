from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-do-not-reveal'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    # blueprint for auth routes in our app
    from .json import json as json_blueprint
    app.register_blueprint(json_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
