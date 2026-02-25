"""Textes de documentation (OpenAPI) pour les endpoints Fidèle.

But: garder les routers lisibles en isolant les descriptions longues.
"""

FIDELE_ADD_STRUCTURE_DESCRIPTION = (
    "Cet endpoint crée l' **appartenance** d'un fidèle à une structure (table `fidele_structure`).\n\n"
    "### Cas d'usage\n"
    "- Un fidèle peut devenir membre d'un mouvement/association/service (ex: GTKI, UJKI, ...).\n"
    "- L'appartenance est une relation entre :\n"
    "  - `id` (path) : l'ID du fidèle\n"
    "  - `body.id_structure` : l'ID de la structure\n\n"
    "### Important: Bureau ecclésiatique (structure id=1)\n"
    "La structure **Bureau ecclésiatique** (id=1) **n'a pas de membres génériques**.\n"
    "Donc l'appartenance via `fidele_structure` est **interdite** pour `id_structure = 1`.\n"
    "Pour rattacher un fidèle à un bureau, utilisez plutôt les **mandats/fonctions** via :\n"
    "- `POST /direction/{id}/fonctions` (table `direction_fonction`)\n\n"
    "### Comportement\n"
    "- Si l'appartenance existe déjà et n'est pas supprimée: retour `400`.\n"
    "- Si l'appartenance existe mais est soft-deleted (`est_supprimee=true`): elle est **restaurée**.\n\n"
    "### Exemple\n"
    "```json\n"
    "{\n"
    "  \"id_structure\": 12\n"
    "}\n"
    "```\n"
)


FIDELE_STATUT_UPDATE_DESCRIPTION = (
    "Cet endpoint met à jour le statut d'un fidèle (`document_statut`).\n\n"
    "### Règles métier\n"
    "- Le code matriculation est attribué uniquement au passage `En attente (id=1)` -> `Validé (id=29)`.\n"
    "- Le champ `id_fidele_recenseur` est requis lors de cette validation.\n"
    "- Les sympathisants (`id_fidele_type=2`) ne reçoivent jamais de code matriculation, même validés.\n"
    "- Format du code fidèle: `ISO_ALPHA_2` + `id_fidele` sur 8 chiffres (10 caractères au total).\n\n"
    "### Exemple\n"
    "- Si la nation de la paroisse active est `CD` et l'id fidèle est `125`, le code est `CD00000125`.\n"
)
