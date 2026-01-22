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

