import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain
import numpy as np
from collections import defaultdict
# Charger les données
df = pd.read_csv('tableaux/jeux_complets.csv')
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df = df[df["Nombre d'avis"] >= 5]
df = df[df["Note Metacritic"].notna()]

# Créer le graphe
G_jeux = nx.Graph()

# Ajouter les nœuds
for index, row in df.iterrows():
    G_jeux.add_node(row['Nom'],Plateformes=row['Plateformes'],Editeur=row['Editeur'],note_meta=row['Note Metacritic'],note_user=row['Note Utilisateur'],Ventes_Total=row['Ventes_Total'], Genres=row['Genres'])

jeux = list(G_jeux.nodes)

# Ajouter les arêtes en fonction des plateformes communes et autres paramètres

for i in range(len(df)):
    jeu1 = jeux[i]
    platforms_i = set(G_jeux.nodes[jeu1]['Plateformes'].split(', '))
    genres_i=set(G_jeux.nodes[jeu1]['Genres'].split(', '))
    for j in range(i + 1, len(df)):
        weight=0
        jeu2 = jeux[j]
        platforms_j = set(G_jeux.nodes[jeu2]['Plateformes'].split(', '))
        common_platforms = platforms_i.intersection(platforms_j)
        if(len(common_platforms)>4):
            weight +=2
        elif(len(common_platforms)>2):
            weight +=1
        genres_j=set(G_jeux.nodes[jeu2]['Genres'].split(', '))
        common_genres = genres_i.intersection(genres_j)
        if(len(common_platforms)>1):
            weight +=1

        # Ajouter des poids basés sur d'autres paramètres
        if G_jeux.nodes[jeu1]['Editeur'] == G_jeux.nodes[jeu2]['Editeur']:
            weight += 1
        if abs(G_jeux.nodes[jeu1]['note_meta'] - G_jeux.nodes[jeu2]['note_meta']) <= 5:
            weight += 1
        if abs(G_jeux.nodes[jeu1]['note_user'] - G_jeux.nodes[jeu2]['note_user']) <= 0.25:
            weight += 1
        if abs(G_jeux.nodes[jeu1]['Ventes_Total'] - G_jeux.nodes[jeu2]['Ventes_Total']) <= 0.5:
            weight += 1
        
        if weight > 0:
            G_jeux.add_edge(jeu1,jeu2, weight=weight)

pos = nx.spring_layout(G_jeux)
nx.draw(G_jeux, pos, node_size=50, with_labels=False)
plt.show()
"""
for i in range(len(df)):
    jeu1 = jeux[i]
    platforms_i = set(G_jeux.nodes[jeu1]['Plateformes'].split(', '))
    genres_i=set(G_jeux.nodes[jeu1]['Genres'].split(', '))
    for j in range(i + 1, len(df)):
        jeu2 = jeux[j]
        platforms_j = set(G_jeux.nodes[jeu2]['Plateformes'].split(', '))
        common_platforms = platforms_i.intersection(platforms_j)

        genres_j=set(G_jeux.nodes[jeu2]['Genres'].split(', '))
        common_genres = genres_i.intersection(genres_j)


        # Ajouter des poids basés sur d'autres paramètres
        
        if(len(common_platforms)>1 or len(common_platforms)>1 or  G_jeux.nodes[jeu1]['Editeur'] == G_jeux.nodes[jeu2]['Editeur'] or abs(G_jeux.nodes[jeu1]['note_meta'] - G_jeux.nodes[jeu2]['note_meta']) <= 5 or abs(G_jeux.nodes[jeu1]['note_user'] - G_jeux.nodes[jeu2]['note_user']) <= 0.25 or abs(G_jeux.nodes[jeu1]['Ventes_Total'] - G_jeux.nodes[jeu2]['Ventes_Total']) <= 0.5):
            G_jeux.add_edge(jeu1,jeu2)
"""
# Afficher le graphe
print("Nombre de sommets:", G_jeux.number_of_nodes())
print("Nombre d'arêtes:", G_jeux.number_of_edges())
"""
plt.figure(figsize=(12, 12))
pos = nx.kamada_kawai_layout(G_jeux)
nx.draw(G_jeux, pos, with_labels=False, node_size=5, width=0.1)
plt.title('Graphe des jeux avant la détection de communauté')
plt.savefig("distance/graphes/graph_avant_communaute.png")
"""
# Algorithme de Louvain
partition = community_louvain.best_partition(G_jeux)

# Afficher le nombre de communautés et leurs membres
communities = {}
for node, community in partition.items():
    if community not in communities:
        communities[community] = []
    communities[community].append(node)

print("Nombre de communautés:", len(communities))
for i, (community, members) in enumerate(communities.items()):
    print(f"Communauté {i + 1}: {members}")


# Visualiser et enregistrer le graphe après la détection de communauté
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(G_jeux, k=0.15, iterations=20)
colors = ['r', 'g', 'b', 'y', 'c', 'm', 'orange', 'purple', 'pink', 'brown', 'lime', 'cyan']
for i, (community, members) in enumerate(communities.items()):
    nx.draw_networkx_nodes(G_jeux, pos, nodelist=members, node_color=colors[i % len(colors)], label=f'Communauté {i + 1}', node_size=50)
nx.draw_networkx_edges(G_jeux, pos, alpha=0.1)  # Réduire l'opacité des arêtes
plt.title('Graphe des jeux après la détection de communauté')
plt.legend(fontsize=8)
plt.savefig("distance/graphes/graph_apres_communaute.png")
plt.show()


# Organiser les nœuds par communauté
community_nodes = defaultdict(list)
for node, comm_id in partition.items():
    community_nodes[comm_id].append(node)

with open('distance/community_analysis.txt', 'w') as f:
    for comm_id, nodes_list in community_nodes.items():
        f.write(f"Communauté {comm_id} contient {len(nodes_list)} noeuds.\n")
        degs = [G_jeux.degree(n) for n in nodes_list]
        f.write(f"Degré moyen : {np.mean(degs)}\n")
        f.write(f"Variance du degré : {np.var(degs)}\n")
        f.write("-----\n")


# Enregistrer les communautés dans un fichier CSV
community_df = pd.DataFrame([(node, comm_id) for comm_id, nodes_list in community_nodes.items() for node in nodes_list], columns=['Jeu', 'Communauté'])
community_df.to_csv('distance/communities.csv', index=False)

# Calculer les statistiques pour chaque communauté  
for comm_id, nodes_list in community_nodes.items():
    print(f"Communauté {comm_id} contient {len(nodes_list)} noeuds.")
    degs = [G_jeux.degree(n) for n in nodes_list]
    print("Degré moyen :", np.mean(degs))
    print("Variance du degré :", np.var(degs))
    print("-----")
#fichier
with open('distance/community_analysis.txt', 'w') as f:
    for comm_id, nodes_list in community_nodes.items():
        f.write(f"Communauté {comm_id} contient {len(nodes_list)} noeuds.\n")
        degs = [G_jeux.degree(n) for n in nodes_list]
        f.write(f"Degré moyen : {np.mean(degs)}\n")
        f.write(f"Variance du degré : {np.var(degs)}\n")
        f.write("-----\n")

