"""Textes de documentation (OpenAPI) pour les endpoints Paroisse.

But: garder les routers lisibles en isolant les descriptions longues.
"""

PAROISSE_LIST_FIDELES_DESCRIPTION = (
    "Cet endpoint retourne les fidèles d'une paroisse via l'historique `fidele_paroisse`.\n\n"
    "### Filtre `actif` (par défaut: `true`)\n"
    "- `actif=true` : retourne uniquement les appartenances **actives actuellement** (`est_actif=true`).\n"
    "- `actif=false` : retourne les appartenances **non actives** (`est_actif=false`).\n\n"
    "- `actif=None` : retourne **toutes** les appartenances (actives + non actives).\n\n"
    "### Règles appliquées\n"
    "- Les lignes soft-delete (`est_supprimee=true`) sont toujours exclues.\n"
    "- La pagination est disponible via `offset` et `limit`.\n\n"
    "### Exemple\n"
    "- `GET /paroisse/{id}/fidele` → actifs uniquement (par défaut).\n"
    "- `GET /paroisse/{id}/fidele?actif=false` → historique non actif.\n"
    "- `GET /paroisse/{id}/fidele?actif=` (None) → actifs + non actifs.\n"
)


PAROISSE_CREATE_DESCRIPTION = (
    "Cet endpoint crée une paroisse et attribue automatiquement son code matriculation.\n\n"
    "### Règle de génération\n"
    "- Préfixe: `PRS` (code du `document_type` PAROISSE)\n"
    "- Suffixe: `id_paroisse` sur 7 chiffres avec zero-padding\n"
    "- Taille totale: 10 caractères\n\n"
    "### Exemple\n"
    "- Si l'id paroisse vaut `123`, le code généré est `PRS0000123`.\n"
)
