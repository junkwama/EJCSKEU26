"""add_fidele_rencensement_statut

Revision ID: 4caffec833e8
Revises: 14607bbf4981
Create Date: 2026-03-13 14:06:20.121980

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4caffec833e8'
down_revision = '14607bbf4981'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('fidele', sa.Column('rencensement_statut', sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column('fidele', 'rencensement_statut')
