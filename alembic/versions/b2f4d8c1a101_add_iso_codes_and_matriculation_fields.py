"""add iso codes and matriculation fields

Revision ID: b2f4d8c1a101
Revises: 9f2a2885b963
Create Date: 2026-02-25 11:00:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = "b2f4d8c1a101"
down_revision = "9f2a2885b963"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    def has_column(table_name: str, column_name: str) -> bool:
        return any(col["name"] == column_name for col in inspector.get_columns(table_name))

    def has_unique_constraint(table_name: str, constraint_name: str) -> bool:
        return any(
            uq.get("name") == constraint_name for uq in inspector.get_unique_constraints(table_name)
        )

    def has_foreign_key(table_name: str, fk_name: str) -> bool:
        return any(fk.get("name") == fk_name for fk in inspector.get_foreign_keys(table_name))

    op.execute(
        "INSERT IGNORE INTO document_statut (id, nom, description, id_document_type) "
        "VALUES (29, 'Validé', 'Document validé', NULL)"
    )

    if not has_column("nation", "iso_alpha_2"):
        op.add_column("nation", sa.Column("iso_alpha_2", sa.String(length=2), nullable=True))

    if not has_column("document_type", "code"):
        op.add_column("document_type", sa.Column("code", sa.String(length=3), nullable=True))
    op.execute("UPDATE document_type SET code = 'FDL' WHERE id = 1")
    op.execute("UPDATE document_type SET code = 'STR' WHERE id = 2")
    op.execute("UPDATE document_type SET code = 'PRS' WHERE id = 3")
    op.execute("UPDATE document_type SET code = 'VLL' WHERE id = 4")
    op.execute("UPDATE document_type SET code = 'PRV' WHERE id = 5")
    op.execute("UPDATE document_type SET code = 'NTN' WHERE id = 6")
    op.execute("UPDATE document_type SET code = 'CTN' WHERE id = 7")
    op.execute("UPDATE document_type SET code = 'GNR' WHERE id = 8")
    if has_column("document_type", "code"):
        op.alter_column(
            "document_type",
            "code",
            existing_type=sa.String(length=3),
            nullable=False,
        )
    if not has_unique_constraint("document_type", "uq_document_type_code"):
        op.create_unique_constraint("uq_document_type_code", "document_type", ["code"])

    if not has_column("paroisse", "code_matriculation"):
        op.add_column("paroisse", sa.Column("code_matriculation", sa.String(length=10), nullable=True))
    if not has_unique_constraint("paroisse", "uq_paroisse_code_matriculation"):
        op.create_unique_constraint(
            "uq_paroisse_code_matriculation", "paroisse", ["code_matriculation"]
        )

    if not has_column("fidele", "id_document_statut"):
        op.add_column("fidele", sa.Column("id_document_statut", sa.Integer(), nullable=True))
    if not has_column("fidele", "code_matriculation"):
        op.add_column("fidele", sa.Column("code_matriculation", sa.String(length=10), nullable=True))
    op.execute("UPDATE fidele SET id_document_statut = 1 WHERE id_document_statut IS NULL")
    if has_column("fidele", "id_document_statut"):
        op.alter_column(
            "fidele",
            "id_document_statut",
            existing_type=sa.Integer(),
            nullable=False,
        )
    if not has_foreign_key("fidele", "fk_fidele_document_statut"):
        op.create_foreign_key(
            "fk_fidele_document_statut",
            "fidele",
            "document_statut",
            ["id_document_statut"],
            ["id"],
            ondelete="RESTRICT",
        )
    if not has_unique_constraint("fidele", "uq_fidele_code_matriculation"):
        op.create_unique_constraint("uq_fidele_code_matriculation", "fidele", ["code_matriculation"])


def downgrade() -> None:
    op.drop_constraint("uq_fidele_code_matriculation", "fidele", type_="unique")
    op.drop_constraint("fk_fidele_document_statut", "fidele", type_="foreignkey")
    op.drop_column("fidele", "code_matriculation")
    op.drop_column("fidele", "id_document_statut")

    op.drop_constraint("uq_paroisse_code_matriculation", "paroisse", type_="unique")
    op.drop_column("paroisse", "code_matriculation")

    op.drop_constraint("uq_document_type_code", "document_type", type_="unique")
    op.drop_column("document_type", "code")

    op.drop_column("nation", "iso_alpha_2")
