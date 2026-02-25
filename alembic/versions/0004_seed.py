"""Seed reference (constant) data.

Revision ID: 0004_seed
Revises: 9be1f9db74bf
Create Date: 2026-02-16 15:00:00.000000

This migration re-seeds reference data after the addition of new table "document_statut". The seed data is inserted
by executing the SQL in `alembic/seed/initial_data.sql`. 
"""

from __future__ import annotations

from pathlib import Path

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

# revision identifiers, used by Alembic.
revision = "0004_seed"
# So that the schema migration runs before this seed.
down_revision = "9be1f9db74bf"
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
        try:
            bind.execute(sa.text(stmt))
        except SQLAlchemyError as exc:
            msg = str(exc)
            is_future_column_seed = (
                "Unknown column" in msg
                and ("iso_alpha_2" in msg or "document_type" in msg and "code" in msg)
            )
            if is_future_column_seed:
                continue
            raise


def downgrade() -> None:
    # Reference data downgrade is intentionally a no-op.
    pass
