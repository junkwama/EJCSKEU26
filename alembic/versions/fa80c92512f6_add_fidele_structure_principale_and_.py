"""add_fidele_structure_principale_and_refactor_matricule

Revision ID: fa80c92512f6
Revises: baa7e9faf8fd
Create Date: 2026-03-13 15:13:08.776618

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'fa80c92512f6'
down_revision = 'baa7e9faf8fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'fidele_structure',
        sa.Column('est_structure_principale', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    op.execute(
        """
        UPDATE fidele_structure fs
        INNER JOIN (
            SELECT id_fidele, MIN(id) AS min_id
            FROM fidele_structure
            WHERE est_supprimee = 0
            GROUP BY id_fidele
        ) picked ON picked.min_id = fs.id
        SET fs.est_structure_principale = 1
        """
    )

    op.alter_column(
        'fidele',
        'code_matriculation',
        existing_type=mysql.VARCHAR(length=10),
        type_=sa.String(length=12),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'fidele',
        'code_matriculation',
        existing_type=sa.String(length=12),
        type_=mysql.VARCHAR(length=10),
        existing_nullable=True,
    )

    op.drop_column('fidele_structure', 'est_structure_principale')
