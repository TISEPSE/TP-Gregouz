import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import url_for, redirect, request
from src.db import get_connection

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

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sessions (session_id, user_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (session_id, user_id, created_at.isoformat(), expires_at.isoformat()),
        )
        conn.commit()

    return session_id


def get_session(session_id: str) -> dict | None:
    """
    Récupère les données d'une session.
    Retourne None si la session n'existe pas ou a expiré.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_id, created_at, expires_at
            FROM sessions
            WHERE session_id = ?
            """,
            (session_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    session = {
        "user_id": row[0],
        "created_at": datetime.fromisoformat(row[1]),
        "expires_at": datetime.fromisoformat(row[2]),
    }

    # Vérifier si la session a expiré
    if datetime.now() > session["expires_at"]:
        delete_session(session_id)
        return None

    return session


def delete_session(session_id: str) -> bool:
    """
    Supprime une session (déconnexion).
    Retourne True si la session existait.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        return cursor.rowcount > 0

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
