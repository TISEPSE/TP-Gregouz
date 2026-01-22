from flask import Blueprint, session, url_for, flash, render_template
from src.services.users import get_user

info_blueprint = Blueprint("infos", __name__)

#============Render Route============#

@info_blueprint.get("/infos")
def informations():
    return render_template("Informations.html")

