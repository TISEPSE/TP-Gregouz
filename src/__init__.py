from flask import Flask
import os

from src.forms import forms_blueprint
from src.auth import auth_blueprint


def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
    app.register_blueprint(forms_blueprint)
    app.register_blueprint(auth_blueprint)
    return app