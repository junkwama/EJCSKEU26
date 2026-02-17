from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy import engine_from_config, pool

from sqlmodel import SQLModel

# Alembic Config object
config = context.config

# Configure logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use env var for DB URL (do not store secrets in alembic.ini)
# Alembic runs migrations synchronously; use the sync driver URL here.
try:
    from dotenv import load_dotenv

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    load_dotenv(os.path.join(project_root, ".env"))
except Exception:
    # If python-dotenv isn't installed, we'll rely on the process environment.
    pass

db_url = os.getenv("MYSQL_DB_SYNC_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

if not config.get_main_option("sqlalchemy.url"):
    raise RuntimeError(
        "No database URL configured for Alembic. Set MYSQL_DB_SYNC_URL in .env or the environment."
    )

# IMPORTANT: import models so SQLModel.metadata is populated
import models.adresse
import models.contact
import models.constants
import models.direction
import models.direction.fonction
import models.fidele
import models.paroisse

#service modules
from modules.file.models import File


target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
