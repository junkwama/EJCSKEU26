"""Seed reference (constant) data.

Revision ID: 0002_seed_reference_data
Revises: 0001_init_schema
Create Date: 2026-02-13

This migration seeds *required* reference data (lookup tables) that the app
expects to exist by executing the SQL in `alembic/seed/initial_data.sql`.

Important:
- This revision is intentionally self-contained (no imports from app code).
- IDs are seeded explicitly inside the SQL file to match the app's enum expectations.

Before using this revision in a real chain, set `down_revision` to your
"init schema" revision id so the schema is created before the inserts.
"""

from __future__ import annotations

from pathlib import Path

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002_seed_reference_data"
# TODO: set this to your init-schema revision id (e.g. "0001_init_schema")
# so that the schema migration runs before this seed.
down_revision = "0001_init_schema"
branch_labels = None
depends_on = None


def _iter_sql_statements(sql_text: str) -> list[str]:
    # Remove full-line comments and join; then split on ';'
    lines: list[str] = []
    for raw in sql_text.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith("--"):
            continue
        lines.append(raw)

    joined = "\n".join(lines)
    statements = [s.strip() for s in joined.split(";")]
    return [s for s in statements if s]


def upgrade() -> None:
    seed_path = Path(__file__).resolve().parents[1] / "seed" / "initial_data.sql"
    if not seed_path.exists():
        raise RuntimeError(f"Seed file not found: {seed_path}")

    sql_text = seed_path.read_text(encoding="utf-8")
    bind = op.get_bind()
    for stmt in _iter_sql_statements(sql_text):
        bind.execute(sa.text(stmt))


def downgrade() -> None:
    # Reference data downgrade is intentionally a no-op.
    pass
