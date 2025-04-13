import pandas as pd

# Charger les données du fichier CSV des communautés
df_communities = pd.read_csv('distance/docs/v8_annalyse_communautes.csv')

# Calculer le total pour chaque genre
total_genres = df_communities['Genres'].apply(eval).apply(lambda x: pd.Series(x)).sum()

# Calculer le total pour chaque plateforme
total_plateformes = df_communities['Plateformes'].apply(eval).apply(lambda x: pd.Series(x)).sum()

# Calculer le total pour chaque éditeur
total_editeurs = df_communities['Éditeurs'].apply(eval).apply(lambda x: pd.Series(x)).sum()

# Calculer le total pour chaque année de parution
total_annees = df_communities['Années de parution'].apply(eval).apply(lambda x: pd.Series(x)).sum()

# Calculer le total pour chaque répartition des ventes
total_ventes = df_communities['Répartition des ventes'].apply(eval).apply(lambda x: pd.Series(x)).sum()

# Enregistrer les totaux dans un CSV
totals = pd.concat([total_genres, total_plateformes, total_editeurs, total_annees, total_ventes], axis=1, keys=['Total Genres', 'Total Plateformes', 'Total Éditeurs', 'Total Années de Parution', 'Total Répartition des Ventes'])
totals.to_csv('totals_all_values.csv')

# Afficher les résultats
print("Totaux pour chaque valeur enregistrés dans totals_all_values.csv")
print(totals)

# Calculer les pourcentages pour chaque communauté pour chaque valeur
percentages_genres = df_communities['Genres'].apply(eval).apply(lambda x: pd.Series(x)).div(total_genres, axis=1) * 100
percentages_plateformes = df_communities['Plateformes'].apply(eval).apply(lambda x: pd.Series(x)).div(total_plateformes, axis=1) * 100
percentages_editeurs = df_communities['Éditeurs'].apply(eval).apply(lambda x: pd.Series(x)).div(total_editeurs, axis=1) * 100
percentages_annees = df_communities['Années de parution'].apply(eval).apply(lambda x: pd.Series(x)).div(total_annees, axis=1) * 100
percentages_ventes = df_communities['Répartition des ventes'].apply(eval).apply(lambda x: pd.Series(x)).div(total_ventes, axis=1) * 100

# Enregistrer les pourcentages dans un CSV
percentages = pd.concat([percentages_genres, percentages_plateformes, percentages_editeurs, percentages_annees, percentages_ventes], axis=1, keys=['Pourcentage Genres', 'Pourcentage Plateformes', 'Pourcentage Éditeurs', 'Pourcentage Années de Parution', 'Pourcentage Répartition des Ventes'])
percentages.to_csv('percentages_all_values.csv')

# Afficher les résultats
print("Pourcentages pour chaque communauté pour chaque valeur enregistrés dans percentages_all_values.csv")
print(percentages)

# Créer des tableaux différents pour chaque catégorie
tables = {
    'Genres': percentages_genres,
    'Plateformes': percentages_plateformes,
    'Éditeurs': percentages_editeurs,
    'Années de Parution': percentages_annees,
    'Répartition des Ventes': percentages_ventes
}

# Enregistrer les tableaux dans un seul fichier Excel
with open('totals_all_categories.csv', 'w') as f:
    for category, data in tables.items():
        f.write(f"{category}\n")
        data.to_csv(f, header=True)
        f.write("\n")

# Afficher les résultats
print("Tableaux différents pour chaque catégorie enregistrés dans totals_all_categories.xlsx")
