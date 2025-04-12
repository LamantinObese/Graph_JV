import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv('jeux_complets.csv')

# Filtrer les jeux qui ont à la fois une note utilisateur et une note Metacritic
df = df.dropna(subset=['Note Utilisateur', 'Note Metacritic'])

# Réinitialiser les indices après avoir filtré les lignes
df = df.reset_index(drop=True)

# Normaliser les notes utilisateur (sur 5) et Metacritic (sur 100) pour qu'elles soient sur la même échelle
df['Note Utilisateur Normalisée'] = df['Note Utilisateur'] * 20  # Convertir la note utilisateur sur 100
df['Note Metacritic Normalisée'] = df['Note Metacritic']  # La note Metacritic est déjà sur 100

# Créer une matrice de similarité basée sur la différence absolue entre les notes normalisées
similarity_matrix = np.zeros((len(df), len(df)))

# Ajouter un indicateur de progression
total_iterations = len(df) * (len(df) - 1) // 2  # Nombre total de paires à traiter
current_iteration = 0

print("Début du calcul des similarités...")

for i in range(len(df)):
    for j in range(i + 1, len(df)):
        # Calculer la différence absolue entre les notes normalisées
        diff = abs(df.loc[i, 'Note Utilisateur Normalisée'] - df.loc[j, 'Note Utilisateur Normalisée']) + \
               abs(df.loc[i, 'Note Metacritic Normalisée'] - df.loc[j, 'Note Metacritic Normalisée'])
        similarity_matrix[i, j] = diff
        similarity_matrix[j, i] = diff

        # Afficher la progression
        current_iteration += 1
        if current_iteration % 1000 == 0:  # Afficher la progression toutes les 1000 paires
            print(f"Progression : {current_iteration}/{total_iterations} paires traitées ({current_iteration / total_iterations * 100:.2f}%)")

print("Calcul des similarités terminé.")

# Définir un seuil de similarité pour créer des liens
seuil_similarite = 5  # Vous pouvez ajuster ce seuil selon vos besoins

# Créer une liste de liens
liens = []
print("Création des liens...")

for i in range(len(df)):
    for j in range(i + 1, len(df)):
        if similarity_matrix[i, j] <= seuil_similarite:
            liens.append({
                'Source': df.loc[i, 'ID'],
                'Target': df.loc[j, 'ID'],
                'Weight': 1 - (similarity_matrix[i, j] / 100)  # Poids basé sur la similarité
            })

# Convertir la liste de liens en DataFrame
df_liens = pd.DataFrame(liens)

# Sauvegarder le DataFrame en tant que fichier CSV
df_liens.to_csv('liens_similarite_notes.csv', index=False)

print("Fichier CSV des liens généré avec succès.")