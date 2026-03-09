"""expand fidele password column for argon2 hashes

Revision ID: aa72d5c1e9f1
Revises: d1c6e8a9f2b4
Create Date: 2026-03-09 11:45:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "aa72d5c1e9f1"
down_revision = "d1c6e8a9f2b4"
branch_labels = None
depends_on = None


def _get_column_type(table_name: str, column_name: str):
    bind = op.get_bind()
    inspector = inspect(bind)
    for column in inspector.get_columns(table_name):
        if column.get("name") == column_name:
            return column.get("type")
    return None


def upgrade() -> None:
    current_type = _get_column_type("fidele", "password")
    current_length = getattr(current_type, "length", None)

    if current_length is None or current_length < 255:
        op.alter_column(
            "fidele",
            "password",
            existing_type=sa.String(length=current_length or 64),
            type_=sa.String(length=255),
            existing_nullable=True,
        )


def downgrade() -> None:
    current_type = _get_column_type("fidele", "password")
    current_length = getattr(current_type, "length", None)

    if current_length is None or current_length > 64:
        op.alter_column(
            "fidele",
            "password",
            existing_type=sa.String(length=current_length or 255),
            type_=sa.String(length=64),
            existing_nullable=True,
        )
