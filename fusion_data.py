import pandas as pd

# 1. Charger les données
games_data = pd.read_csv("games_data_50000.csv")
vgsales = pd.read_csv("vgsales.csv")

# 2. Nettoyer et uniformiser les noms
games_data["Nom"] = games_data["Nom"].str.strip().str.title()
vgsales["Name"] = vgsales["Name"].str.strip().str.title()

# 3. Fonction pour obtenir l'éditeur le plus fréquent
def get_most_common_publisher(x):
    modes = x.mode()
    return modes[0] if not modes.empty else x.iloc[0]

# 4. Agrégation des données de vente
aggregated_sales = vgsales.groupby("Name").agg({
    "Global_Sales": "sum",
    "Publisher": get_most_common_publisher,
    "Year": "min"
}).reset_index()

# 5. Fusion en gardant uniquement les jeux présents dans les deux tableaux
final_data = games_data.merge(
    aggregated_sales,
    left_on="Nom",
    right_on="Name",
    how="inner"  # Changement de 'left' à 'inner' pour l'intersection
).drop(columns=["Name"])

# 6. Supprimer le .0 des années et convertir en entier
final_data["Year"] = final_data["Year"].fillna(0).astype(int).replace(0, pd.NA)

# 7. Renommer et sélectionner les colonnes
final_data = final_data.rename(columns={
    "Global_Sales": "Ventes_Total",
    "Publisher": "Editeur",
    "Year": "Annee_Parution"
})

output_columns = [
    "ID", "Nom", "Note Metacritic", "Note Utilisateur", "Nombre d'avis",
    "Plateformes", "Genres", "Tags", "Ventes_Total", "Editeur", "Annee_Parution"
]
final_data = final_data[output_columns]

# 8. Sauvegarder
final_data.to_csv("jeux_complets.csv", index=False, encoding="utf-8")
print(f"Fichier généré avec succès! {len(final_data)} jeux communs trouvés.")