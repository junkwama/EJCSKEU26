from pathlib import Path
import re
import unicodedata

path = Path('/Users/judynkwama/Downloads/project-ejcsk26/ejcsk26-api/alembic/seed/initial_data.sql')
lines = path.read_text(encoding='utf-8').splitlines()

explicit = {
    'République Démocratique du Congo': 'CD',
    'Congo': 'CG',
    'France': 'FR',
    'Belgique': 'BE',
    'États-Unis': 'US',
    'Canada': 'CA',
    'Afrique du Sud': 'ZA',
    'Angola': 'AO',
    'Burundi': 'BI',
    'Rwanda': 'RW',
    'Cameroun': 'CM',
    "Côte d'Ivoire": 'CI',
    'Gabon': 'GA',
    'Kenya': 'KE',
    'Nigeria': 'NG',
    'Tanzanie': 'TZ',
    'Ouganda': 'UG',
    'Zambie': 'ZM',
    'Zimbabwe': 'ZW',
    'Royaume-Uni': 'GB',
    'Italie': 'IT',
    'Allemagne': 'DE',
    'Espagne': 'ES',
    'Portugal': 'PT',
    'Brésil': 'BR',
    'Argentine': 'AR',
    'Mexique': 'MX',
    'Chine': 'CN',
    'Japon': 'JP',
    'Inde': 'IN',
}

pattern = re.compile(r"^INSERT IGNORE INTO nation \(nom, id_continent\) VALUES \('((?:[^']|'')*)',\s*(\d+)\);$")


def default_iso(name: str) -> str:
    cleaned = ''.join(ch for ch in unicodedata.normalize('NFKD', name) if ord(ch) < 128)
    cleaned = re.sub(r'[^A-Za-z]', '', cleaned).upper()
    if len(cleaned) >= 2:
        return cleaned[:2]
    if len(cleaned) == 1:
        return cleaned + 'X'
    return 'XX'

out = []
skip_old_iso_block = False
for line in lines:
    if line.startswith('-- Hydratation du code ISO alpha-2 des nations'):
        skip_old_iso_block = True
        continue

    if skip_old_iso_block:
        if line.startswith('-- Structure types'):
            skip_old_iso_block = False
            out.append(line)
        continue

    m = pattern.match(line)
    if not m:
        out.append(line)
        continue

    raw_name, id_continent = m.groups()
    nation_name = raw_name.replace("''", "'")
    iso = explicit.get(nation_name, default_iso(nation_name))
    out.append(
        f"INSERT IGNORE INTO nation (nom, id_continent, iso_alpha_2) VALUES ('{raw_name}', {id_continent}, '{iso}');"
    )

path.write_text('\n'.join(out) + '\n', encoding='utf-8')
print('Seed nations rewritten with iso_alpha_2 inline.')
