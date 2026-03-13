"""change_fidele_rencensement_statut_to_integer_percentage

Revision ID: baa7e9faf8fd
Revises: 4caffec833e8
Create Date: 2026-03-13 14:17:18.789696

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'baa7e9faf8fd'
down_revision = '4caffec833e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE fidele
        SET rencensement_statut = CASE
            WHEN JSON_TYPE(rencensement_statut) = 'OBJECT'
                THEN CAST(JSON_UNQUOTE(JSON_EXTRACT(rencensement_statut, '$.completion_percentage')) AS UNSIGNED)
            WHEN JSON_TYPE(rencensement_statut) IN ('INTEGER', 'DOUBLE')
                THEN CAST(JSON_UNQUOTE(JSON_EXTRACT(rencensement_statut, '$')) AS UNSIGNED)
            ELSE NULL
        END
        WHERE rencensement_statut IS NOT NULL
        """
    )
    op.alter_column(
        'fidele',
        'rencensement_statut',
        existing_type=mysql.JSON(),
        type_=sa.Integer(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        'fidele',
        'rencensement_statut',
        existing_type=sa.Integer(),
        type_=mysql.JSON(),
        existing_nullable=True,
    )
    op.execute(
        """
        UPDATE fidele
        SET rencensement_statut = JSON_OBJECT(
            'is_completed', IF(rencensement_statut >= 100, TRUE, FALSE),
            'completed_steps', NULL,
            'total_steps', NULL,
            'completion_percentage', rencensement_statut
        )
        WHERE rencensement_statut IS NOT NULL
        """
    )
