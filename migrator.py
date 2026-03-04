import argparse
import os
import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = "users.sqlite"
MIGRATIONS_DIR = "migrations"


def get_connection():
    return sqlite3.connect(DB_PATH)


def ensure_version_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migrator_version (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def get_current_version(conn):
    ensure_version_table(conn)
    row = conn.execute("SELECT version FROM migrator_version LIMIT 1").fetchone()
    return row[0] if row else None


def set_current_version(conn, version):
    conn.execute("DELETE FROM migrator_version")
    if version is not None:
        conn.execute(
            "INSERT INTO migrator_version (version, applied_at) VALUES (?, ?)",
            (version, datetime.now().isoformat()),
        )
    conn.commit()


def list_migration_files(migrations_dir):
    if not migrations_dir.exists():
        return []
    files = [f for f in os.listdir(migrations_dir) if f.endswith(".sql")]
    return sorted(files)


def parse_migration_file(path):
    content = path.read_text(encoding="utf-8")

    if "-- UP" not in content or "-- DOWN" not in content:
        raise ValueError(f"Migration invalide (marqueurs manquants): {path.name}")

    up_part, down_part = content.split("-- DOWN", 1)
    up_sql = up_part.replace("-- UP", "", 1).strip()
    down_sql = down_part.strip()

    if not up_sql:
        raise ValueError(f"Migration invalide (section UP vide): {path.name}")
    if not down_sql:
        raise ValueError(f"Migration invalide (section DOWN vide): {path.name}")

    return up_sql, down_sql


def extract_version(filename):
    return filename.split("_", 1)[0]


def cmd_status():
    migrations_dir = Path.cwd() / MIGRATIONS_DIR
    files = list_migration_files(migrations_dir)

    with get_connection() as conn:
        current_version = get_current_version(conn)

    print("Version    Fichier                                        Statut")
    print("----------------------------------------------------------------------")
    for filename in files:
        version = extract_version(filename)
        status = "en attente"
        if current_version is not None and version <= current_version:
            status = "appliquée"
        print(f"{version:<10} {filename:<45} {status}")


def cmd_up():
    migrations_dir = Path.cwd() / MIGRATIONS_DIR
    files = list_migration_files(migrations_dir)

    with get_connection() as conn:
        current_version = get_current_version(conn)
        pending = [f for f in files if current_version is None or extract_version(f) > current_version]

        if not pending:
            print("Aucune migration en attente.")
            return

        count = 0
        for filename in pending:
            path = migrations_dir / filename
            up_sql, _ = parse_migration_file(path)
            version = extract_version(filename)

            print(f"Applying {filename}...")
            conn.executescript(up_sql)
            set_current_version(conn, version)
            print("  -> OK")
            count += 1

    print(f"\n{count} migration(s) appliquée(s).")


def cmd_down():
    migrations_dir = Path.cwd() / MIGRATIONS_DIR
    files = list_migration_files(migrations_dir)
    by_version = {extract_version(f): f for f in files}
    ordered_versions = [extract_version(f) for f in files]

    with get_connection() as conn:
        current_version = get_current_version(conn)
        if current_version is None:
            print("Aucune migration appliquée.")
            return

        filename = by_version.get(current_version)
        if filename is None:
            raise ValueError(f"Fichier de migration introuvable pour la version {current_version}")

        _, down_sql = parse_migration_file(migrations_dir / filename)
        print(f"Rollback {filename}...")
        conn.executescript(down_sql)

        idx = ordered_versions.index(current_version)
        previous_version = ordered_versions[idx - 1] if idx > 0 else None
        set_current_version(conn, previous_version)
        print("  -> OK")


def slugify(name):
    return "_".join(name.strip().lower().split())


def cmd_create(name):
    migrations_dir = Path.cwd() / MIGRATIONS_DIR
    migrations_dir.mkdir(parents=True, exist_ok=True)
    files = list_migration_files(migrations_dir)

    if files:
        last_version = int(extract_version(files[-1]))
        next_version = f"{last_version + 1:03d}"
    else:
        next_version = "001"

    filename = f"{next_version}_{slugify(name)}.sql"
    path = migrations_dir / filename

    content = "-- UP\n\n-- DOWN\n"
    path.write_text(content, encoding="utf-8")
    print(f"Migration créée: {path}")


def build_parser():
    parser = argparse.ArgumentParser(description="Migrator SQLite simplifié")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")
    subparsers.add_parser("up")
    subparsers.add_parser("down")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("name", help="Nom descriptif de la migration")

    return parser


def main():
    args = build_parser().parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "up":
        cmd_up()
    elif args.command == "down":
        cmd_down()
    elif args.command == "create":
        cmd_create(args.name)


if __name__ == "__main__":
    main()
