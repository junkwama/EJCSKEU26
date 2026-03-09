"""move id_etat_civile from fidele to fidele_famille

Revision ID: 4bf8c9a7d1e2
Revises: a8c1f9d4e2b7
Create Date: 2026-03-09 10:15:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "4bf8c9a7d1e2"
down_revision = "a8c1f9d4e2b7"
branch_labels = None
depends_on = None


def _get_columns(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = inspect(bind)
    return {column["name"] for column in inspector.get_columns(table_name)}


def _get_indexes(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = inspect(bind)
    return {item.get("name") for item in inspector.get_indexes(table_name) if item.get("name")}


def _get_foreign_keys(table_name: str) -> list[dict]:
    bind = op.get_bind()
    inspector = inspect(bind)
    return inspector.get_foreign_keys(table_name)


def _drop_fk_for_column(table_name: str, column_name: str) -> None:
    for fk in _get_foreign_keys(table_name):
        constrained = fk.get("constrained_columns") or []
        fk_name = fk.get("name")
        if column_name in constrained and fk_name:
            op.drop_constraint(fk_name, table_name, type_="foreignkey")


def upgrade() -> None:
    bind = op.get_bind()

    columns_fidele = _get_columns("fidele")
    columns_famille = _get_columns("fidele_famille")

    if "id_etat_civile" not in columns_famille:
        op.add_column("fidele_famille", sa.Column("id_etat_civile", sa.Integer(), nullable=True))

    indexes_famille = _get_indexes("fidele_famille")
    if "idx_fidele_famille_etat_civile" not in indexes_famille:
        op.create_index("idx_fidele_famille_etat_civile", "fidele_famille", ["id_etat_civile"], unique=False)

    columns_fidele = _get_columns("fidele")
    if "id_etat_civile" in columns_fidele:
        bind.execute(sa.text(
            """
            INSERT INTO fidele_famille (
                id_fidele,
                id_etat_civile,
                est_supprimee,
                date_creation,
                date_modification
            )
            SELECT
                f.id,
                f.id_etat_civile,
                0,
                UTC_TIMESTAMP(),
                UTC_TIMESTAMP()
            FROM fidele f
            LEFT JOIN fidele_famille ff ON ff.id_fidele = f.id
            WHERE ff.id IS NULL
              AND f.id_etat_civile IS NOT NULL
            """
        ))

        bind.execute(sa.text(
            """
            UPDATE fidele_famille ff
            JOIN fidele f ON f.id = ff.id_fidele
            SET ff.id_etat_civile = COALESCE(ff.id_etat_civile, f.id_etat_civile)
            WHERE ff.id_etat_civile IS NULL
              AND f.id_etat_civile IS NOT NULL
            """
        ))

    null_count = bind.execute(sa.text("SELECT COUNT(*) FROM fidele_famille WHERE id_etat_civile IS NULL")).scalar()
    if null_count and null_count > 0:
        default_etat_id = bind.execute(sa.text("SELECT MIN(id) FROM etat_civile")).scalar()
        if default_etat_id is None:
            raise RuntimeError("Cannot enforce NOT NULL on fidele_famille.id_etat_civile: etat_civile is empty")
        bind.execute(
            sa.text("UPDATE fidele_famille SET id_etat_civile = :default_etat_id WHERE id_etat_civile IS NULL"),
            {"default_etat_id": int(default_etat_id)},
        )

    fk_names = {fk.get("name") for fk in _get_foreign_keys("fidele_famille") if fk.get("name")}
    if "fk_fidele_famille_id_etat_civile" not in fk_names:
        op.create_foreign_key(
            "fk_fidele_famille_id_etat_civile",
            "fidele_famille",
            "etat_civile",
            ["id_etat_civile"],
            ["id"],
            ondelete="RESTRICT",
        )

    op.alter_column(
        "fidele_famille",
        "id_etat_civile",
        existing_type=sa.Integer(),
        nullable=False,
    )

    columns_fidele = _get_columns("fidele")
    if "id_etat_civile" in columns_fidele:
        _drop_fk_for_column("fidele", "id_etat_civile")
        op.drop_column("fidele", "id_etat_civile")


def downgrade() -> None:
    bind = op.get_bind()

    columns_fidele = _get_columns("fidele")
    columns_famille = _get_columns("fidele_famille")

    if "id_etat_civile" not in columns_fidele:
        op.add_column("fidele", sa.Column("id_etat_civile", sa.Integer(), nullable=True))

    fidele_fk_names = {fk.get("name") for fk in _get_foreign_keys("fidele") if fk.get("name")}
    if "fk_fidele_id_etat_civile" not in fidele_fk_names:
        op.create_foreign_key(
            "fk_fidele_id_etat_civile",
            "fidele",
            "etat_civile",
            ["id_etat_civile"],
            ["id"],
            ondelete="SET NULL",
        )

    if "id_etat_civile" in columns_famille:
        bind.execute(sa.text(
            """
            UPDATE fidele f
            LEFT JOIN fidele_famille ff ON ff.id_fidele = f.id AND ff.est_supprimee = 0
            SET f.id_etat_civile = COALESCE(f.id_etat_civile, ff.id_etat_civile)
            """
        ))

        bind.execute(sa.text(
            """
            UPDATE fidele f
            JOIN (
                SELECT id_fidele, MAX(id_etat_civile) AS id_etat_civile
                FROM fidele_famille
                WHERE id_etat_civile IS NOT NULL
                GROUP BY id_fidele
            ) t ON t.id_fidele = f.id
            SET f.id_etat_civile = COALESCE(f.id_etat_civile, t.id_etat_civile)
            """
        ))

    if "id_etat_civile" in columns_famille:
        _drop_fk_for_column("fidele_famille", "id_etat_civile")

        indexes_famille = _get_indexes("fidele_famille")
        if "idx_fidele_famille_etat_civile" in indexes_famille:
            op.drop_index("idx_fidele_famille_etat_civile", table_name="fidele_famille")

        op.drop_column("fidele_famille", "id_etat_civile")
