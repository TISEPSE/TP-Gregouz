from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.db import USERS

auth_blueprint = Blueprint("auth", __name__)


#============Register Route============#

@auth_blueprint.get("/register")
def register_get():
    return render_template("register.html")


@auth_blueprint.post("/register")
def register():
    form = request.form.to_dict()
    password = form.get("password")
    username = form.get("username")

    if username in USERS:
        return redirect(url_for("auth.register_get"))

    secure_password = generate_password_hash(password)
    print(f"Mot de passe de base => {password} : Mot de passe hashé: {secure_password}")

    USERS[username] = secure_password
    
    # Afficher tous les utilisateurs enregistrés du dictionnaire
    print("\n=== Utilisateurs enregistrés ===")
    for username in USERS:
        print(f"Utilisateur: {username}, Mot de passe: {USERS[username]}")
    print("=" * 32 + "\n")
    
    flash(f"Utilisateur {username} créé avec succès !", "success")
    
#==============Login Route==============#

@auth_blueprint.get("/login")
def login_get():
    return render_template("login.html")

@auth_blueprint.post("/login")
def login():
    username = request.form.get("email")
    password = request.form.get("password")

    if username not in USERS:
        return redirect(url_for("auth.login_get"))

    print(f"Email reçu: {username}, Mot de passe reçu: {password}")

    return render_template("login.html")