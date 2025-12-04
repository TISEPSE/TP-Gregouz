from flask import Blueprint, render_template, request

auth_blueprint = Blueprint("auth", __name__)


#============Register Route============#

@auth_blueprint.get("/register")
def register_get():
    return render_template("register.html")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    mot_de_passe = request.form.get("password")
    print(f"Email reçu: {email}, Mot de passe reçu: {mot_de_passe}")
    return render_template("register.html")

#==============Login Route==============#

@auth_blueprint.get("/login")
def login_get():
    return render_template("login.html")

@auth_blueprint.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    mot_de_passe = request.form.get("password")
    print(f"Email reçu: {email}, Mot de passe reçu: {mot_de_passe}")
    return render_template("login.html")