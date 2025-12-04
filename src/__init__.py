from flask import Flask

from src.forms import forms_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(forms_blueprint)
    return app