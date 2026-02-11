from flask import Blueprint, render_template, redirect, url_for, request
from src.services.sessions import get_current_user

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
def index():
    current_user = get_current_user(request)
    if current_user:
        return redirect(url_for("dashboard.home"))
    return render_template("dashboard.html", user=None)
