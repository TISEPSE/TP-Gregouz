from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.services.users import add_user, is_user_in_db, get_user
from src.services.sessions import create_session, delete_session, get_session

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
        return redirect(url_for("auth.register_get"))
    
    elif add_user(username, secure_password):
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
    
    session_id = create_session(username)

    response = redirect(url_for("dashboard.home"))
    response.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        samesite="Lax",
        max_age="86400",
        secure=True
    )
    
    secure_password = user[2]

    if check_password_hash(secure_password, password):
        session["name"] = username
        flash("Connexion réussie", "success")
        return redirect('/')
    else: 
        flash("Mot de passe incorrect", "error")
        return redirect(url_for("auth.login_page"))
    

#==============Logout Route==============#

@auth_blueprint.get("/logout")
def logout():
    # Récupérer le session_id depuis le cookie
    session_id = request.cookies.get("session_id")

    if session_id:
        # Supprimer la session côté serveur
        delete_session(session_id)

    # Créer une réponse qui supprime le cookie
    response = redirect(url_for("auth.login_page"))
    response.delete_cookie("session_id")
    flash("Déconnexion réussie", "success")

    return response
