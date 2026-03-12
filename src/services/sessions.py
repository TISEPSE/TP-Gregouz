import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import url_for, redirect, request
from src.db import db
from src.models import Session

# Durée de vie d'une session
SESSION_LIFETIME = timedelta(minutes=1440)

def login_required(f):
    """
    Décorateur qui protège une route.
    Redirige vers /login si l'utilisateur n'est pas connecté.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user(request)
        if not current_user:
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)
    return decorated_function


def generate_session_id():
    """
    Génère un identifiant de session sécurisé.
    secrets.token_hex génère une chaîne aléatoire cryptographiquement sûre.
    """
    return secrets.token_hex(32)  # 64 caractères hexadécimaux


def create_session(user_id: str) -> str:
    """
    Crée une nouvelle session pour un utilisateur.
    Retourne le session_id à stocker dans le cookie.
    """
    session_id = generate_session_id()
    created_at = datetime.now()
    expires_at = created_at + SESSION_LIFETIME

    session = Session(
        session_id=session_id,
        user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
    )
    db.session.add(session)
    db.session.commit()

    return session_id


def get_session(session_id: str) -> dict | None:
    """
    Récupère les données d'une session.
    Retourne None si la session n'existe pas ou a expiré.
    """
    session = db.session.query(Session).filter_by(session_id=session_id).first()
    if session is None:
        return None

    payload = {
        "user_id": session.user_id,
        "created_at": session.created_at,
        "expires_at": session.expires_at,
    }

    # Vérifier si la session a expiré
    if datetime.now() > payload["expires_at"]:
        delete_session(session_id)
        return None

    return payload


def delete_session(session_id: str) -> bool:
    """
    Supprime une session (déconnexion).
    Retourne True si la session existait.
    """
    deleted = db.session.query(Session).filter_by(session_id=session_id).delete()
    db.session.commit()
    return deleted > 0

def get_current_user(request) -> str | None:
    """
    Récupère l'utilisateur actuellement connecté à partir de la requête.
    Retourne None si l'utilisateur n'est pas connecté.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None

    session = get_session(session_id)
    if not session:
        return None

    return session["user_id"]
