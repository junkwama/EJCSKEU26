"""add document_type superior hierarchy

Revision ID: 6ab1e2d3f4c5
Revises: aa72d5c1e9f1
Create Date: 2026-03-11 12:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "6ab1e2d3f4c5"
down_revision = "aa72d5c1e9f1"
branch_labels = None
depends_on = None


TABLE_NAME = "document_type"
COLUMN_NAME = "id_document_type_superieur"
FK_NAME = "fk_document_type_superieur"


def _has_column(inspector, table_name: str, column_name: str) -> bool:
    return any(col.get("name") == column_name for col in inspector.get_columns(table_name))


def _has_fk(inspector, table_name: str, fk_name: str) -> bool:
    for fk in inspector.get_foreign_keys(table_name):
        if fk.get("name") == fk_name:
            return True
    return False


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if not _has_column(inspector, TABLE_NAME, COLUMN_NAME):
        op.add_column(TABLE_NAME, sa.Column(COLUMN_NAME, sa.Integer(), nullable=True))

    # Hierarchie complete: GENERALE -> CONTINENT -> NATION -> PROVINCE -> VILLE -> PAROISSE -> STRUCTURE -> FIDELE
    bind.execute(
        sa.text(
            """
            UPDATE document_type
            SET id_document_type_superieur = CASE id
                WHEN 1 THEN 2
                WHEN 2 THEN 3
                WHEN 3 THEN 4
                WHEN 4 THEN 5
                WHEN 5 THEN 6
                WHEN 6 THEN 7
                WHEN 7 THEN 8
                WHEN 8 THEN NULL
                ELSE id_document_type_superieur
            END
            """
        )
    )

    inspector = inspect(bind)
    if not _has_fk(inspector, TABLE_NAME, FK_NAME):
        op.create_foreign_key(
            FK_NAME,
            TABLE_NAME,
            TABLE_NAME,
            [COLUMN_NAME],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if _has_fk(inspector, TABLE_NAME, FK_NAME):
        op.drop_constraint(FK_NAME, TABLE_NAME, type_="foreignkey")

    inspector = inspect(bind)
    if _has_column(inspector, TABLE_NAME, COLUMN_NAME):
        op.drop_column(TABLE_NAME, COLUMN_NAME)
