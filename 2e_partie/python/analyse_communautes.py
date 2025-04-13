import pandas as pd
import numpy as np
from collections import defaultdict

input_csv='tableaux/jeux_complets.csv'
community_csv='distance/communities.csv'
output_txt='distance/docs/annalyse_communautes.txt'
output_csv='distance/docs/annalyse_communautes.csv' 
# Charger les données des jeux
df = pd.read_csv(input_csv)

# Charger les données des communautés
community_df = pd.read_csv(community_csv)

# Organiser les nœuds par communauté
community_nodes = defaultdict(list)
for index, row in community_df.iterrows():
    community_nodes[row['Communauté']].append(row['Jeu'])

# Calculer les statistiques pour chaque communauté et enregistrer dans un fichier
with open(output_txt, 'w') as f:
    for comm_id, nodes_list in community_nodes.items():
        f.write(f"Communauté {comm_id} contient {len(nodes_list)} noeuds.\n")
        degs = [df[df['Nom'] == n]['Note Utilisateur'].values[0] for n in nodes_list]
        f.write(f"Degré moyen : {np.mean(degs)}\n")
        f.write(f"Variance du degré : {np.var(degs)}\n")

        # Analyser les jeux dans la communauté
        genres = defaultdict(int)
        editeurs = defaultdict(int)
        annees = defaultdict(int)
        ventes = {'<100k': 0, '100k-1M': 0, '1M-10M': 0, '>10M': 0}
        plateformes = defaultdict(int)
        for node in nodes_list:
            genre_list = df[df['Nom'] == node]['Genres'].values[0].split(', ')
            for genre in genre_list:
                genres[genre] += 1
                
            editeur_values = df[df['Nom'] == node]['Editeur'].values
            if len(editeur_values) > 0:
                editeurs[editeur_values[0]] += 1
            
            annee_values = df[df['Nom'] == node]['Annee_Parution'].values
            if len(annee_values) > 0:
                annees[annee_values[0]] += 1
            
            ventes_total_values = df[df['Nom'] == node]['Ventes_Total'].values
            if len(ventes_total_values) > 0:
                ventes_total = ventes_total_values[0]
                if ventes_total < 0.1:
                    ventes['<100k'] += 1
                elif ventes_total < 1:
                    ventes['100k-1M'] += 1
                elif ventes_total < 10:
                    ventes['1M-10M'] += 1
                else:
                    ventes['>10M'] += 1
                
            plateforme_list = df[df['Nom'] == node]['Plateformes'].values[0].split(', ')
            for plateforme in plateforme_list:
                plateformes[plateforme] += 1
        f.write("-----\n")
        f.write("Genres les plus fréquents :\n")
        for genre, count in sorted(genres.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{genre}: {count}\n")
        f.write("-----\n")
        f.write("Éditeurs les plus fréquents :\n")
        for editeur, count in sorted(editeurs.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{editeur}: {count}\n")
        f.write("-----\n")
        f.write("Années de parution les plus fréquentes :\n")
        for annee, count in sorted(annees.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{annee}: {count}\n")
        f.write("-----\n")
        f.write("Répartition des ventes :\n")
        for range_ventes, count in sorted(ventes.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{range_ventes}: {count}\n")
        f.write("-----\n")
        f.write("Plateformes les plus fréquentes :\n")
        for plateforme, count in sorted(plateformes.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{plateforme}: {count}\n")

        f.write("-----\n")
        f.write("-----\n")

    # Enregistrer les communautés dans un fichier CSV avec les informations triées par ordre décroissant de présence
    community_info = []
    for comm_id, nodes_list in community_nodes.items():
        genres = defaultdict(int)
        editeurs = defaultdict(int)
        annees = defaultdict(int)
        ventes = {'<100k': 0, '100k-1M': 0, '1M-10M': 0, '>10M': 0}
        plateformes = defaultdict(int)
        for node in nodes_list:
            genre_list = df[df['Nom'] == node]['Genres'].values[0].split(', ')
            for genre in genre_list:
                genres[genre] += 1
            
            editeur_values = df[df['Nom'] == node]['Editeur'].values
            if len(editeur_values) > 0:
                editeurs[editeur_values[0]] += 1
            
            annee_values = df[df['Nom'] == node]['Annee_Parution'].values
            if len(annee_values) > 0:
                annees[annee_values[0]] += 1
            
            ventes_total_values = df[df['Nom'] == node]['Ventes_Total'].values
            if len(ventes_total_values) > 0:
                ventes_total = ventes_total_values[0]
                if ventes_total < 0.1:
                    ventes['<100k'] += 1
                elif ventes_total < 1:
                    ventes['100k-1M'] += 1
                elif ventes_total < 10:
                    ventes['1M-10M'] += 1
                else:
                    ventes['>10M'] += 1
            
            plateforme_list = df[df['Nom'] == node]['Plateformes'].values[0].split(', ')
            for plateforme in plateforme_list:
                plateformes[plateforme] += 1

        community_info.append({
            'Communauté': comm_id,
            'Nombre de noeuds': len(nodes_list),
            'Genres': dict(sorted(genres.items(), key=lambda item: item[1], reverse=True)),
            'Éditeurs': dict(sorted(editeurs.items(), key=lambda item: item[1], reverse=True)),
            'Années de parution': dict(sorted(annees.items(), key=lambda item: item[1], reverse=True)),
            'Répartition des ventes': dict(sorted(ventes.items(), key=lambda item: item[1], reverse=True)),
            'Plateformes': dict(sorted(plateformes.items(), key=lambda item: item[1], reverse=True))
        })


community_info_df = pd.DataFrame(community_info)
community_info_df.to_csv(output_csv, index=False)



print("Les informations ont été enregistrées dans le fichier community_analysis.txt.")
