from flask import Blueprint, session, url_for, render_template, redirect
from src.services.users import get_user
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

info_blueprint = Blueprint("infos", __name__)

#============Render Route============#

@info_blueprint.get("/infos")
def informations():
    username = session.get("name")
    if not username:
        return redirect(url_for("auth.login_page"))

    user = get_user(username)

    # Formate les timestamps en français
    created_dt = datetime.strptime(user[3], "%Y-%m-%d %H:%M:%S")
    created_formatted = created_dt.strftime("%d %B %Y à %Hh%M")

    updated_dt = datetime.strptime(user[4], "%Y-%m-%d %H:%M:%S")
    updated_formatted = updated_dt.strftime("%d %B %Y à %Hh%M")

    return render_template("Informations.html",
                           user_id=user[0],
                           user_name=user[1],
                           user_password=user[2],
                           user_created=created_formatted,
                           user_updated=updated_formatted)