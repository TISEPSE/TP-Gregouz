from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.users import add_user, is_user_in_db, get_user

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

    if is_user_in_db(username):
        flash("L'utilisateur existe déjà", "error")
        print("L'utilisateur existe déjà en base")
        return redirect(url_for("auth.register_get"))
    
    elif add_user(username, secure_password):
        print("Utilisateur ajouter à la base de donnée")
        flash("Inscription réussie !", "success")
        return redirect(url_for('auth.login_page'))
    
    else:
        flash("Erreur lors de l'inscription", "error")
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
        flash("Utilisateur non trouvé", "error")
        return redirect(url_for("auth.login_page"))
    
    secure_password = user[2]

    if check_password_hash(secure_password, password):
        # Stocker le message dans la session pour l'afficher sur la page suivante
        session['login_success_message'] = "Connexion réussie"
        return redirect('/')
    else: 
        flash("Mot de passe incorrect", "error")
        return redirect(url_for("auth.login_page"))