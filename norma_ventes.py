import pandas as pd

# Charger le fichier original
df = pd.read_csv('jeux_complets.csv')

# Vérification que les colonnes nécessaires existent
if 'ID' not in df.columns or 'Ventes_Total' not in df.columns:
    raise ValueError("Le fichier doit contenir les colonnes 'Id' et 'Ventes_Total'")

# Conversion des millions en unités individuelles
df['ventes_unités'] = df['Ventes_Total'] * 1_000_000

# Création des catégories
def categoriser_ventes(ventes):
    if ventes >= 10_000_000:
        return "10M+"
    elif ventes >= 1_000_000:
        return "1M-10M"
    elif ventes >= 100_000:
        return "100K-1M"
    elif ventes >= 10_000:
        return "10K-100K"
    elif ventes >= 1_000:
        return "1K-10K"
    else:
        return "<1K"

# Application de la catégorisation
df['Catégorie_Ventes'] = df['ventes_unités'].apply(categoriser_ventes)

# Création du fichier de sortie
resultat = df[['ID', 'Catégorie_Ventes']]

# Sauvegarde
resultat.to_csv('ventes_par_catégorie.csv', index=False)

print("Fichier généré avec succès !")
print("Exemple de données :")
print(resultat.head())