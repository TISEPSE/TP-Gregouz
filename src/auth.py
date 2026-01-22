from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.users import add_user

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

    secure_password = generate_password_hash(password)
    print(f"User crée: '{username}'")
    print(f"Mot de passe de base => {password} : Mot de passe hashé: {secure_password}")

    if add_user(username, secure_password):
        print("Utilisateur ajouter à la base de donnée")
        return redirect(url_for('auth.login_page'))
    else:
        return redirect(url_for("auth.register_get"))
    
    
#==============Login Route==============#

@auth_blueprint.get("/login")
def login_page():
    return render_template("login.html")

@auth_blueprint.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = get_user(username)
    if user is None:
        return redirect(url_for("auth.login_page"))
    
    secure_password = user[2]

    if check_password_hash(secure_password, password):
        return redirect('/')
    else: 
        return redirect(url_for("auth.login_page"))