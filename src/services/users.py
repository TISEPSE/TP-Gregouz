from sqlalchemy.exc import IntegrityError

from src.db import db
from src.models import User

# --- Insert ---

def add_user(name, password):
    """"Ajoute un utilisateur dans la base de donnée"""
    try:
        user = User(name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        print("Ce nom d'utilisateur existe déja")
        return False

# --- Select ---

def is_user_in_db(name):
    """Vérifie si l'utilisateur existe déja dans la base de donnée."""
    return db.session.query(User.id).filter_by(name=name).first() is not None

def get_user(name):
    """Récupère toutes les infos d'un users en cherchant son nom"""
    return db.session.query(User).filter_by(name=name).first()
    
