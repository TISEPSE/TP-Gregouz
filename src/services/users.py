import sqlite3
import os

DB_PATH = "/home/baptiste/Vscode/TP-Gregouz/users.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

# --- Insert ---

def add_user(name, password):
    """"Ajoute un utilisateur dans la base de donnée"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, password) VALUES (?,?)", (name, password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print("Ce nom d'utilisateur existe déja")
        return False

# --- Select ---

def is_user_in_db(name):
    """Vérifie si l'utilisateur existe déja dans la base de donnée."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_user(name):
    """Récupère toutes les infos d'un users en cherchant son nom"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password, created_at, updated_at FROM users WHERE name = ?", (name,))
        return cursor.fetchone()
