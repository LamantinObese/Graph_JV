import pandas as pd
from collections import OrderedDict

# Charger le fichier CSV
df = pd.read_csv('jeux_complets.csv')

# Définir les catégories de plateformes avec les noms exacts de la base
platform_categories = OrderedDict([
    ('pc', ['PC', 'macOS', 'Linux']),
    ('console', [
        'PlayStation 5', 'PlayStation 4', 'PlayStation 3',
        'Xbox Series S/X', 'Xbox One', 'Xbox 360',
        'Nintendo Switch', 'Wii U', 'Wii'
    ]),
    ('mobile', ['Android', 'iOS']),
    ('portable', ['PS Vita', 'PSP', 'Nintendo 3DS', 'Nintendo DS', 'Nintendo DSi']),
    ('web', ['Web']),
    ('retro', [  # Plateformes sorties avant les années 2000
        'PlayStation 2', 'PlayStation', 'Xbox', 'GameCube',
        'Dreamcast', 'Nintendo 64', 'Game Boy', 'PSP'
    ])
])

# Fonction pour normaliser une plateforme individuelle
def categorize_platform(platform):
    platform = platform.strip()
    for category, keywords in platform_categories.items():
        for keyword in keywords:
            if keyword.lower() == platform.lower():
                return category
    return 'retro'

def normalize_platforms(platforms_str):
    if pd.isna(platforms_str):
        return ''
    
    platforms = [p.strip() for p in platforms_str.split(',')]
    categories = set()
    
    for platform in platforms:
        category = categorize_platform(platform)
        categories.add(category)
    
    # Si plusieurs catégories, on retourne "cross-platform"
    if len(categories) > 1:
        return 'cross-platform'
    elif len(categories) == 1:
        return categories.pop()
    else:
        return ''

# Appliquer la normalisation
df['Plateformes'] = df['Plateformes'].apply(normalize_platforms)

# Sauvegarder le résultat
df.to_csv('games_data_normalized.csv', index=False)

print("Normalisation terminée. Résultat sauvegardé dans 'games_data_normalized.csv'")