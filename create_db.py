from src import create_app
from src.db import db
from src import models  # noqa: F401


def create_database():
    app = create_app()
    with app.app_context():
        db.create_all()
    print(\"Base de données initialisée avec succès !\")

if __name__ == "__main__":
    create_database()
