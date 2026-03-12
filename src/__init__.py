from flask import Flask
import os

from src.routes.dashboard import dashboard_blueprint
from src.routes.auth import auth_blueprint
from src.informations import info_blueprint
from src.routes.home import home_blueprint
from src.db import db


def create_app():
    app = Flask(__name__,template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
    app.secret_key = "une-cle-secrete-au-hasard"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(info_blueprint)
    app.register_blueprint(home_blueprint)
    return app
