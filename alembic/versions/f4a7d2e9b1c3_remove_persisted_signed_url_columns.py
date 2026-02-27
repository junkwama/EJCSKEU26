"""remove persisted signed url columns from file

Revision ID: f4a7d2e9b1c3
Revises: e31a4cd2b7f9
Create Date: 2026-02-26 13:10:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
import sqlmodel


# revision identifiers, used by Alembic.
revision = "f4a7d2e9b1c3"
down_revision = "e31a4cd2b7f9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("file")}

    if "signed_url" in columns:
        op.drop_column("file", "signed_url")

    if "signed_url_expiration_date" in columns:
        op.drop_column("file", "signed_url_expiration_date")


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {column["name"] for column in inspector.get_columns("file")}

    if "signed_url" not in columns:
        op.add_column(
            "file",
            sa.Column("signed_url", sqlmodel.sql.sqltypes.AutoString(length=1000), nullable=True),
        )

    if "signed_url_expiration_date" not in columns:
        op.add_column(
            "file",
            sa.Column("signed_url_expiration_date", sa.DateTime(), nullable=True),
        )
