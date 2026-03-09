"""move bapteme fields and rename origine nation column

Revision ID: a8c1f9d4e2b7
Revises: f4a7d2e9b1c3
Create Date: 2026-03-08 10:40:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "a8c1f9d4e2b7"
down_revision = "f4a7d2e9b1c3"
branch_labels = None
depends_on = None


def _get_columns(table_name: str) -> set[str]:
    bind = op.get_bind()
    inspector = inspect(bind)
    return {column["name"] for column in inspector.get_columns(table_name)}


def _get_unique_constraints(table_name: str) -> dict[str, list[str]]:
    bind = op.get_bind()
    inspector = inspect(bind)
    constraints: dict[str, list[str]] = {}
    for item in inspector.get_unique_constraints(table_name):
        name = item.get("name")
        cols = item.get("column_names") or []
        if name:
            constraints[name] = cols
    return constraints


def _get_indexes(table_name: str) -> dict[str, list[str]]:
    bind = op.get_bind()
    inspector = inspect(bind)
    indexes: dict[str, list[str]] = {}
    for item in inspector.get_indexes(table_name):
        name = item.get("name")
        cols = item.get("column_names") or []
        if name:
            indexes[name] = cols
    return indexes


def upgrade() -> None:
    bind = op.get_bind()
    columns_fidele = _get_columns("fidele")
    columns_bapteme = _get_columns("fidele_bapteme")
    columns_origine = _get_columns("fidele_origine")

    # 1) rename fidele_origine.id_nation -> id_nation_origine
    if "id_nation" in columns_origine and "id_nation_origine" not in columns_origine:
        op.alter_column(
            "fidele_origine",
            "id_nation",
            existing_type=sa.Integer(),
            new_column_name="id_nation_origine",
            existing_nullable=True,
        )

    # rename index if needed
    indexes_origine = _get_indexes("fidele_origine")
    if "idx_fidele_origine_nation" not in indexes_origine and "idx_fidele_origine_nation_origine" not in indexes_origine:
        op.create_index("idx_fidele_origine_nation_origine", "fidele_origine", ["id_nation_origine"], unique=False)

    # 2) add new columns to fidele_bapteme
    if "numero_carte" not in columns_bapteme:
        op.add_column("fidele_bapteme", sa.Column("numero_carte", sa.String(length=50), nullable=True))
    if "date_day" not in columns_bapteme:
        op.add_column("fidele_bapteme", sa.Column("date_day", sa.Integer(), nullable=True))
    if "date_month" not in columns_bapteme:
        op.add_column("fidele_bapteme", sa.Column("date_month", sa.Integer(), nullable=True))
    if "date_year" not in columns_bapteme:
        op.add_column("fidele_bapteme", sa.Column("date_year", sa.Integer(), nullable=True))

    # refresh columns after add
    columns_bapteme = _get_columns("fidele_bapteme")

    # 3) migrate data from fidele -> fidele_bapteme
    if "numero_carte" in columns_fidele or "date_bapteme" in columns_fidele:
        bind.execute(sa.text(
            """
            INSERT INTO fidele_bapteme (
                id_fidele,
                numero_carte,
                date_day,
                date_month,
                date_year,
                est_supprimee,
                date_creation,
                date_modification
            )
            SELECT
                f.id,
                CASE WHEN :has_numero_carte = 1 THEN f.numero_carte ELSE NULL END,
                CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN DAY(f.date_bapteme) ELSE NULL END,
                CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN MONTH(f.date_bapteme) ELSE NULL END,
                CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN YEAR(f.date_bapteme) ELSE NULL END,
                0,
                UTC_TIMESTAMP(),
                UTC_TIMESTAMP()
            FROM fidele f
            LEFT JOIN fidele_bapteme fb ON fb.id_fidele = f.id
            WHERE fb.id IS NULL
              AND (
                (:has_numero_carte = 1 AND f.numero_carte IS NOT NULL)
                OR (:has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL)
              )
            """
        ), {
            "has_numero_carte": 1 if "numero_carte" in columns_fidele else 0,
            "has_date_bapteme": 1 if "date_bapteme" in columns_fidele else 0,
        })

        bind.execute(sa.text(
            """
            UPDATE fidele_bapteme fb
            JOIN fidele f ON f.id = fb.id_fidele
            SET
                fb.numero_carte = COALESCE(fb.numero_carte, CASE WHEN :has_numero_carte = 1 THEN f.numero_carte ELSE NULL END),
                fb.date_day = COALESCE(fb.date_day, CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN DAY(f.date_bapteme) ELSE NULL END),
                fb.date_month = COALESCE(fb.date_month, CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN MONTH(f.date_bapteme) ELSE NULL END),
                fb.date_year = COALESCE(fb.date_year, CASE WHEN :has_date_bapteme = 1 AND f.date_bapteme IS NOT NULL THEN YEAR(f.date_bapteme) ELSE NULL END)
            """
        ), {
            "has_numero_carte": 1 if "numero_carte" in columns_fidele else 0,
            "has_date_bapteme": 1 if "date_bapteme" in columns_fidele else 0,
        })

    # 4) move unique constraint from fidele.numero_carte to fidele_bapteme.numero_carte
    uq_fidele = _get_unique_constraints("fidele")
    if "uq_fidele_numero_carte" in uq_fidele:
        op.drop_constraint("uq_fidele_numero_carte", "fidele", type_="unique")

    uq_bapteme = _get_unique_constraints("fidele_bapteme")
    if "uq_fidele_bapteme_numero_carte" not in uq_bapteme and "numero_carte" in columns_bapteme:
        op.create_unique_constraint("uq_fidele_bapteme_numero_carte", "fidele_bapteme", ["numero_carte"])

    # 5) remove old columns from fidele
    columns_fidele = _get_columns("fidele")
    if "numero_carte" in columns_fidele:
        op.drop_column("fidele", "numero_carte")
    if "date_bapteme" in columns_fidele:
        op.drop_column("fidele", "date_bapteme")


def downgrade() -> None:
    bind = op.get_bind()

    columns_fidele = _get_columns("fidele")
    columns_bapteme = _get_columns("fidele_bapteme")
    columns_origine = _get_columns("fidele_origine")

    # 1) re-add old fidele columns
    if "numero_carte" not in columns_fidele:
        op.add_column("fidele", sa.Column("numero_carte", sa.String(length=50), nullable=True))
    if "date_bapteme" not in columns_fidele:
        op.add_column("fidele", sa.Column("date_bapteme", sa.Date(), nullable=True))

    # 2) copy back from baptême
    columns_bapteme = _get_columns("fidele_bapteme")
    if all(col in columns_bapteme for col in ["numero_carte", "date_day", "date_month", "date_year"]):
        bind.execute(sa.text(
            """
            UPDATE fidele f
            LEFT JOIN fidele_bapteme fb ON fb.id_fidele = f.id AND fb.est_supprimee = 0
            SET
                f.numero_carte = fb.numero_carte,
                f.date_bapteme = CASE
                    WHEN fb.date_year IS NOT NULL AND fb.date_month IS NOT NULL AND fb.date_day IS NOT NULL
                    THEN STR_TO_DATE(CONCAT(fb.date_year, '-', LPAD(fb.date_month, 2, '0'), '-', LPAD(fb.date_day, 2, '0')), '%Y-%m-%d')
                    ELSE NULL
                END
            """
        ))

    # 3) restore unique on fidele.numero_carte and remove unique on bapteme.numero_carte
    uq_bapteme = _get_unique_constraints("fidele_bapteme")
    if "uq_fidele_bapteme_numero_carte" in uq_bapteme:
        op.drop_constraint("uq_fidele_bapteme_numero_carte", "fidele_bapteme", type_="unique")

    uq_fidele = _get_unique_constraints("fidele")
    if "uq_fidele_numero_carte" not in uq_fidele:
        op.create_unique_constraint("uq_fidele_numero_carte", "fidele", ["numero_carte"])

    # 4) drop added baptême columns
    columns_bapteme = _get_columns("fidele_bapteme")
    if "date_year" in columns_bapteme:
        op.drop_column("fidele_bapteme", "date_year")
    if "date_month" in columns_bapteme:
        op.drop_column("fidele_bapteme", "date_month")
    if "date_day" in columns_bapteme:
        op.drop_column("fidele_bapteme", "date_day")
    if "numero_carte" in columns_bapteme:
        op.drop_column("fidele_bapteme", "numero_carte")

    # 5) rename fidele_origine.id_nation_origine -> id_nation
    columns_origine = _get_columns("fidele_origine")
    if "id_nation_origine" in columns_origine and "id_nation" not in columns_origine:
        op.alter_column(
            "fidele_origine",
            "id_nation_origine",
            existing_type=sa.Integer(),
            new_column_name="id_nation",
            existing_nullable=True,
        )

    indexes_origine = _get_indexes("fidele_origine")
    if "idx_fidele_origine_nation" not in indexes_origine and "idx_fidele_origine_nation_origine" not in indexes_origine:
        op.create_index("idx_fidele_origine_nation", "fidele_origine", ["id_nation"], unique=False)
