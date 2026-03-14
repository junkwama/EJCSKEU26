"""enforce unique recensement relations

Revision ID: 1e2f3a4b5c6d
Revises: fa80c92512f6
Create Date: 2026-03-14 10:45:00.000000

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text


# revision identifiers, used by Alembic.
revision = "1e2f3a4b5c6d"
down_revision = "fa80c92512f6"
branch_labels = None
depends_on = None


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def _has_index(table_name: str, index_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)
    return any(idx["name"] == index_name for idx in inspector.get_indexes(table_name))


def _has_unique_constraint(table_name: str, constraint_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)
    return any(cst["name"] == constraint_name for cst in inspector.get_unique_constraints(table_name))


def _has_trigger(trigger_name: str) -> bool:
    bind = op.get_bind()
    result = bind.execute(
        text(
            """
            SELECT COUNT(*)
            FROM information_schema.TRIGGERS
            WHERE TRIGGER_SCHEMA = DATABASE() AND TRIGGER_NAME = :trigger_name
            """
        ),
        {"trigger_name": trigger_name},
    )
    count = result.scalar_one()
    return bool(count)


def upgrade() -> None:
    # 1) Add paroisse principal flag.
    if not _has_column("fidele_paroisse", "est_paroisse_principale"):
        op.add_column(
            "fidele_paroisse",
            sa.Column(
                "est_paroisse_principale",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("0"),
            ),
        )

    # 2) Normalize principal rows before adding DB guards.
    op.execute("UPDATE fidele_structure SET est_structure_principale = 0 WHERE est_supprimee = 0")
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

    op.execute("UPDATE fidele_paroisse SET est_paroisse_principale = 0 WHERE est_supprimee = 0")
    op.execute(
        """
        UPDATE fidele_paroisse fp
        INNER JOIN (
            SELECT id_fidele, MIN(id) AS min_id
            FROM fidele_paroisse
            WHERE est_supprimee = 0
            GROUP BY id_fidele
        ) picked ON picked.min_id = fp.id
        SET fp.est_paroisse_principale = 1
        """
    )

    # 3) Add triggers to enforce one active principal row per fidele.
    if not _has_trigger("trg_fidele_structure_single_principale_insert"):
        op.execute(
            """
            CREATE TRIGGER trg_fidele_structure_single_principale_insert
            BEFORE INSERT ON fidele_structure
            FOR EACH ROW
            BEGIN
                IF NEW.est_supprimee = 0 AND NEW.est_structure_principale = 1 AND EXISTS (
                    SELECT 1
                    FROM fidele_structure fs
                    WHERE fs.id_fidele = NEW.id_fidele
                      AND fs.est_supprimee = 0
                      AND fs.est_structure_principale = 1
                ) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'duplicate principale structure for fidele';
                END IF;
            END
            """
        )

    if not _has_trigger("trg_fidele_structure_single_principale_update"):
        op.execute(
            """
            CREATE TRIGGER trg_fidele_structure_single_principale_update
            BEFORE UPDATE ON fidele_structure
            FOR EACH ROW
            BEGIN
                IF NEW.est_supprimee = 0 AND NEW.est_structure_principale = 1 AND EXISTS (
                    SELECT 1
                    FROM fidele_structure fs
                    WHERE fs.id_fidele = NEW.id_fidele
                      AND fs.est_supprimee = 0
                      AND fs.est_structure_principale = 1
                      AND fs.id <> NEW.id
                ) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'duplicate principale structure for fidele';
                END IF;
            END
            """
        )

    if not _has_trigger("trg_fidele_paroisse_single_principale_insert"):
        op.execute(
            """
            CREATE TRIGGER trg_fidele_paroisse_single_principale_insert
            BEFORE INSERT ON fidele_paroisse
            FOR EACH ROW
            BEGIN
                IF NEW.est_supprimee = 0 AND NEW.est_paroisse_principale = 1 AND EXISTS (
                    SELECT 1
                    FROM fidele_paroisse fp
                    WHERE fp.id_fidele = NEW.id_fidele
                      AND fp.est_supprimee = 0
                      AND fp.est_paroisse_principale = 1
                ) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'duplicate principale paroisse for fidele';
                END IF;
            END
            """
        )

    if not _has_trigger("trg_fidele_paroisse_single_principale_update"):
        op.execute(
            """
            CREATE TRIGGER trg_fidele_paroisse_single_principale_update
            BEFORE UPDATE ON fidele_paroisse
            FOR EACH ROW
            BEGIN
                IF NEW.est_supprimee = 0 AND NEW.est_paroisse_principale = 1 AND EXISTS (
                    SELECT 1
                    FROM fidele_paroisse fp
                    WHERE fp.id_fidele = NEW.id_fidele
                      AND fp.est_supprimee = 0
                      AND fp.est_paroisse_principale = 1
                      AND fp.id <> NEW.id
                ) THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'duplicate principale paroisse for fidele';
                END IF;
            END
            """
        )

    # 4) Clean duplicate contacts/adresses before adding unique constraints.
    op.execute(
        """
        DELETE c1
        FROM contact c1
        INNER JOIN contact c2
            ON c1.id_document_type = c2.id_document_type
           AND c1.id_document = c2.id_document
           AND c1.id > c2.id
        """
    )
    op.execute(
        """
        DELETE a1
        FROM adresse a1
        INNER JOIN adresse a2
            ON a1.id_document_type = a2.id_document_type
           AND a1.id_document = a2.id_document
           AND a1.id > a2.id
        """
    )

    if not _has_unique_constraint("contact", "uq_contact_document"):
        op.create_unique_constraint(
            "uq_contact_document",
            "contact",
            ["id_document_type", "id_document"],
        )
    if not _has_unique_constraint("adresse", "uq_adresse_document"):
        op.create_unique_constraint(
            "uq_adresse_document",
            "adresse",
            ["id_document_type", "id_document"],
        )


def downgrade() -> None:
    if _has_unique_constraint("adresse", "uq_adresse_document"):
        op.drop_constraint("uq_adresse_document", "adresse", type_="unique")
    if _has_unique_constraint("contact", "uq_contact_document"):
        op.drop_constraint("uq_contact_document", "contact", type_="unique")

    op.execute("DROP TRIGGER IF EXISTS trg_fidele_paroisse_single_principale_update")
    op.execute("DROP TRIGGER IF EXISTS trg_fidele_paroisse_single_principale_insert")
    op.execute("DROP TRIGGER IF EXISTS trg_fidele_structure_single_principale_update")
    op.execute("DROP TRIGGER IF EXISTS trg_fidele_structure_single_principale_insert")

    if _has_column("fidele_paroisse", "est_paroisse_principale"):
        op.drop_column("fidele_paroisse", "est_paroisse_principale")
