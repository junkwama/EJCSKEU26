"""add unique constraint on fidele.tel

Revision ID: d1c6e8a9f2b4
Revises: 4bf8c9a7d1e2
Create Date: 2026-03-09 11:10:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "d1c6e8a9f2b4"
down_revision = "4bf8c9a7d1e2"
branch_labels = None
depends_on = None


def _get_unique_constraints(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = inspect(bind)
    return {
        item.get("name")
        for item in inspector.get_unique_constraints(table_name)
        if item.get("name")
    }


def upgrade() -> None:
    bind = op.get_bind()

    duplicates = bind.execute(
        sa.text(
            """
            SELECT tel, COUNT(*) AS total
            FROM fidele
            WHERE tel IS NOT NULL
            GROUP BY tel
            HAVING COUNT(*) > 1
            LIMIT 5
            """
        )
    ).fetchall()

    if duplicates:
        sample = ", ".join(f"{row[0]} (x{row[1]})" for row in duplicates)
        raise RuntimeError(
            "Cannot add unique constraint uq_fidele_tel because duplicate tel values exist: "
            f"{sample}. Clean duplicates first."
        )

    constraints = _get_unique_constraints("fidele")
    if "uq_fidele_tel" not in constraints:
        op.create_unique_constraint("uq_fidele_tel", "fidele", ["tel"])


def downgrade() -> None:
    constraints = _get_unique_constraints("fidele")
    if "uq_fidele_tel" in constraints:
        op.drop_constraint("uq_fidele_tel", "fidele", type_="unique")
