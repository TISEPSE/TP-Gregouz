# TP4 - Script de démo devant le prof

Ce guide est une check-list exécutable, dans l'ordre.

## 1. Préparer le terminal

```bash
cd /home/baptiste/Vscode/TP-Gregouz
source venv/bin/activate
```

## 2. Montrer la structure attendue

```bash
ls -la migrator.py migrations src/services/sessions.py alembic.ini alembic/versions
```

Points à dire:
- `migrator.py` = outil custom demandé (status/up/down/create).
- `migrations/` = migrations SQL avec `-- UP` / `-- DOWN`.
- `src/services/sessions.py` = sessions persistées en base SQLite.
- `alembic/` = partie 4 avec migrations Alembic.

## 3. Partie 2/3 - Migrator custom

### 3.1 Remettre une base propre

```bash
rm -f users.sqlite
```

### 3.2 Vérifier le status avant migration

```bash
python3 migrator.py status
```

Attendu:
- `001_create_users_table.sql` en attente
- `002_create_sessions_table.sql` en attente

### 3.3 Appliquer les migrations

```bash
python3 migrator.py up
python3 migrator.py status
```

Attendu:
- les deux migrations sont appliquées

### 3.4 Vérifier les tables créées

```bash
python3 - <<'PY'
import sqlite3
conn = sqlite3.connect("users.sqlite")
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print([r[0] for r in cur.fetchall()])
cur.execute("SELECT version, applied_at FROM migrator_version")
print(cur.fetchall())
PY
```

Attendu:
- tables `users`, `sessions`, `migrator_version` (et `sqlite_sequence`)
- `migrator_version` contient la dernière version

### 3.5 Tester rollback de la dernière migration

```bash
python3 migrator.py down
python3 migrator.py status
```

Attendu:
- `002` repasse en attente

### 3.6 Réappliquer pour revenir en état final

```bash
python3 migrator.py up
```

## 4. Montrer `create` (commande demandée)

```bash
python3 migrator.py create "demo migration"
ls -la migrations
rm -f migrations/003_demo_migration.sql
```

Point à dire:
- la commande crée bien le prochain numéro automatiquement.

## 5. Partie 3 - Sessions persistées en DB

```bash
python - <<'PY'
from src.services.sessions import create_session, get_session, delete_session
sid = create_session("demo_user")
print("session_id:", sid)
print("session_exists:", get_session(sid) is not None)
print("deleted:", delete_session(sid))
print("session_after_delete:", get_session(sid) is None)
PY
```

Point à dire:
- avant: dictionnaire en mémoire (perdu au redémarrage)
- maintenant: table `sessions` SQLite, donc persistant

## 6. Partie 4 - Alembic

### 6.1 Repartir de zéro sur `db.sqlite`

```bash
rm -f db.sqlite
```

### 6.2 Appliquer toutes les migrations Alembic

```bash
alembic upgrade head
```

### 6.3 Vérifier version courante + historique

```bash
alembic current
alembic history --verbose
```

### 6.4 Tester rollback puis ré-application

```bash
alembic downgrade -1
alembic current
alembic upgrade head
alembic current
```

Attendu:
- downgrade enlève la migration `sessions`
- upgrade remonte à `head`

## 7. Fichiers clés à montrer rapidement

- `migrator.py`
- `migrations/001_create_users_table.sql`
- `migrations/002_create_sessions_table.sql`
- `src/services/sessions.py`
- `alembic.ini`
- `alembic/versions/559c82cc57b2_create_users_table.py`
- `alembic/versions/e6470c92095b_create_sessions_table.py`

## 8. Résumé oral (30 secondes)

- J’ai implémenté un migrator custom SQLite avec `status/up/down/create`.
- J’ai créé 2 migrations SQL (`users`, `sessions`) avec sections `UP/DOWN`.
- J’ai remplacé le stockage mémoire des sessions par SQLite.
- J’ai aussi mis en place Alembic, créé 2 révisions, et testé `upgrade/downgrade/current/history`.
