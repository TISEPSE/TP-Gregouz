from flask import Blueprint, render_template, request
from werkzeug.security import check_password_hash, generate_password_hash

auth_blueprint = Blueprint("auth", __name__)


#============Register Route============#

@auth_blueprint.get("/register")
def register_get():
    return render_template("register.html")


@auth_blueprint.post("/register")
def register():
    form = request.form.to_dict()
    password = form.get("password")
    secure_password = generate_password_hash(password)
    print(f"Mot de passe de base => {password} : Mot de passe hashé: {secure_password}")
    return render_template("register.html")

#==============Login Route==============#

@auth_blueprint.get("/login")
def login_get():
    return render_template("login.html")

@auth_blueprint.post("/login")
def login():
    email = request.form.get("email")
    mot_de_passe = request.form.get("password")
    print(f"Email reçu: {email}, Mot de passe reçu: {mot_de_passe}")
    return render_template("login.html")