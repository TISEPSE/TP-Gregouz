from logging.config import fileConfig

from alembic import context

from src import create_app
from src.db import db
from src import models  # noqa: F401  # ensure models are imported

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic needs SQLAlchemy metadata
target_metadata = db.metadata


def _get_app_context():
    app = create_app()
    return app.app_context()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    with _get_app_context():
        url = config.get_main_option("sqlalchemy.url")
        if not url:
            url = db.engine.url.render_as_string(hide_password=False)
            config.set_main_option("sqlalchemy.url", url)

        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    with _get_app_context():
        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
