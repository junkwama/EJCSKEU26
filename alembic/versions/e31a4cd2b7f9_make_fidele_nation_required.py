"""make fidele nation required

Revision ID: e31a4cd2b7f9
Revises: c7f1e2a9d4b3
Create Date: 2026-02-26 10:20:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "e31a4cd2b7f9"
down_revision = "c7f1e2a9d4b3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    null_count = bind.execute(
        sa.text("SELECT COUNT(*) FROM fidele WHERE id_nation_nationalite IS NULL")
    ).scalar_one()

    if null_count and int(null_count) > 0:
        raise RuntimeError(
            "Impossible de rendre id_nation_nationalite obligatoire: "
            f"{null_count} fidèle(s) n'ont pas de nationalité. "
            "Veuillez corriger les données puis relancer la migration."
        )

    current_fk_name = None
    for fk in inspector.get_foreign_keys("fidele"):
        constrained_columns = fk.get("constrained_columns") or []
        if constrained_columns == ["id_nation_nationalite"]:
            current_fk_name = fk.get("name")
            break

    if current_fk_name:
        op.drop_constraint(current_fk_name, "fidele", type_="foreignkey")

    op.alter_column(
        "fidele",
        "id_nation_nationalite",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_fidele_nation_nationalite",
        "fidele",
        "nation",
        ["id_nation_nationalite"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_fidele_nation_nationalite", "fidele", type_="foreignkey")

    op.alter_column(
        "fidele",
        "id_nation_nationalite",
        existing_type=sa.Integer(),
        nullable=True,
    )

    op.create_foreign_key(
        "fk_fidele_nation_nationalite",
        "fidele",
        "nation",
        ["id_nation_nationalite"],
        ["id"],
        ondelete="SET NULL",
    )
