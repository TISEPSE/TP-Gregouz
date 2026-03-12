# Réponses

1. Lancer make build une première fois :
   - La commande échoue avec le message "make: *** Aucune règle pour fabriquer la cible « build ». Arrêt." et un code de sortie 2. Il n'y a pas de cible nommée build dans le Makefile. Ce Makefile ne définit que les cibles hello, run et clean.

2. Lancer make build une deuxième fois :
   - Le résultat est identique à la première fois. Make ne trouve toujours pas la cible build, car rien n'a changé dans le Makefile. Il affiche le même message d'erreur.

3. Lancer make sans argument :
   - Make exécute la première cible définie dans le Makefile, qui est hello. Cela compile le fichier hello.c en un exécutable nommé hello en utilisant gcc avec les options spécifiées (-Wall -Wextra -std=c11).

4. Existe-t-il une commande make pour lister toutes les recipes disponibles ?
   - J'ai pas trouvé mais c'est possible.

---

# Exercice 1

1. En vous inspirant de examples/makefile/Makefile, créer un makefile a la racine du projet avec une commande pour lancer le projet: ✅ 

1. En option, rajouter une commande pour nettoyer le projet (supprimer le venv et les fichiers temporaires): ✅ 

1. En option, rajouter une option pour installer les dépendances de dev: ✅

2. Comment éviter que si un utilisateur écrive make sans argument que cela ne lance une commande involontairement ?
   - Make exécute la première cible du fichier par défaut. En mettant `all` en premier avec un message, `make` sans argument affichera juste l'aide sans rien lancer.

---

# Gestion de projet python

1. Comment faire en sorte d'installer uniquement les dépendances requises en production ? Par exemple pytest, une dependance pour lancer des tests, n'est pas necessaire en prod mais est necessaire pour dev.
   - On sépare en deux fichiers : `requirements.txt` (prod uniquement) et `requirements-dev.txt` (dev, qui contient `-r requirements.txt` + pytest etc.). En prod on fait `pip install -r requirements.txt`, en dev `pip install -r requirements-dev.txt`.

&nbsp;

2. Si j'utilise flask version 3.1.2 et que Flask décide de modifier cette version en la supprimant et en poussant une version avec le meme numéro mais du code différent, comment le détecter ?
   - En utilisant des hashes dans le `requirements.txt` via `pip install --require-hashes`. On génère les hashes avec `pip-compile --generate-hashes` (outil `pip-tools`). Si le hash du paquet téléchargé ne correspond pas, pip refuse l'installation.

&nbsp;

3. Il faut que chaque developpeur pense bien à créer un environnement virtuel. Comment s'assurer que chaque developpeur utilise la meme version de python ?
   - On utilise un fichier `.python-version` à la racine du projet (lu par `pyenv`). Tous les développeurs ayant pyenv installé utiliseront automatiquement la version spécifiée. On peut aussi le préciser dans `pyproject.toml` avec `requires-python = "==3.12.*"`.

&nbsp;

4. Alice installe les dependances le 23 fevrier. Bob installe les dependances le 3 mars. Vis a vis du fichier requirements.txt ils ont bien les memes versions mais ils observent quand meme des comportements différents. Pourquoi ?
   - Les dépendances de leurs dépendances (dépendances transitives) ont changé entre les deux dates. Par exemple Flask 3.1.2 dépend de Werkzeug sans version fixée, et Werkzeug a peut-être été mis à jour entre les deux installations. La solution : utiliser `pip freeze > requirements.txt` pour figer **toutes** les versions, y compris les transitives.

---

# Flask-SQLAlchemy

Flask‑SQLAlchemy sert à intégrer SQLAlchemy à Flask avec une configuration centralisée (URI, options) et une gestion automatique du contexte d’application. Concrètement, il fournit un objet `db` partagé, le `db.Model` pour définir les modèles, et un `db.session` déjà scoped à la requête, ce qui simplifie l’accès à la base dans tout le projet.
