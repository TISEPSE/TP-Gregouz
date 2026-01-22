import sqlite3

DB_PATH = ("users.sqlite")

def get_connection():
    return sqlite3.connect(DB_PATH)