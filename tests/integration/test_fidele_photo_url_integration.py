from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def _insert_minimum_fidele_and_photo(async_db_url: str) -> None:
    engine = create_async_engine(async_db_url)
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                INSERT INTO fidele (
                    nom, prenom, sexe, date_naissance, est_baptise, tel,
                    id_grade, id_fidele_type, id_nation_nationalite, id_document_statut,
                    est_supprimee, date_creation, date_modification
                ) VALUES (
                    :nom, :prenom, :sexe, :date_naissance, :est_baptise, :tel,
                    :id_grade, :id_fidele_type, :id_nation_nationalite, :id_document_statut,
                    0, NOW(), NOW()
                )
                """
            ),
            {
                "nom": "Testeur",
                "prenom": "Integration",
                "sexe": "M",
                "date_naissance": "1990-01-01",
                "est_baptise": 1,
                "tel": "+243900000001",
                "id_grade": 1,
                "id_fidele_type": 1,
                "id_nation_nationalite": 170,
                "id_document_statut": 1,
            },
        )

        inserted_id_result = await conn.execute(text("SELECT MAX(id) AS id FROM fidele"))
        fidele_id = inserted_id_result.first().id

        await conn.execute(
            text(
                """
                INSERT INTO file (
                    original_name, file_name, mimetype, size,
                    id_document_type, id_document,
                    est_supprimee, date_creation, date_modification
                ) VALUES (
                    :original_name, :file_name, :mimetype, :size,
                    :id_document_type, :id_document,
                    0, NOW(), NOW()
                )
                """
            ),
            {
                "original_name": "photo.jpg",
                "file_name": f"fidele/{fidele_id}/fidele_{fidele_id}_photo.jpg",
                "mimetype": "image/jpeg",
                "size": 128,
                "id_document_type": 1,
                "id_document": fidele_id,
            },
        )

    await engine.dispose()


def test_fidele_list_include_photo_url_returns_signed_url(app_client):
    import os
    import asyncio

    async_db_url = os.environ["MYSQL_DB_ASYNC_URL"]
    asyncio.run(_insert_minimum_fidele_and_photo(async_db_url))

    response = app_client.get("/fidele?offset=0&limit=10&include=photo_url")
    assert response.status_code == 200

    payload = response.json()
    assert payload["code"] == 200
    assert len(payload["data"]) >= 1

    matched = [item for item in payload["data"] if item.get("nom") == "Testeur"]
    assert matched, "Inserted fidele not returned"
    assert matched[0].get("photo_url") is not None
    assert "X-Amz-Algorithm" in matched[0]["photo_url"]
