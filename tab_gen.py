import requests
import pandas as pd
import time

API_KEY = "fd1ccf0289a94abdac6d8189c2853abe"
BASE_URL = "https://api.rawg.io/api/games"

def fetch_games(api_key, page=1, page_size=20):
    """ Récupère les données des jeux depuis l'API RAWG """
    params = {
        "key": api_key,
        "page": page,
        "page_size": page_size  # Nombre de jeux par page (max 40 par requête)
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur lors de la requête :", response.status_code)
        return None

def parse_game_data(data):
    """ Parse les données des jeux en un tableau (DataFrame) """
    games = []
    for game in data.get("results", []):
        games.append({
            "ID": game.get("id"),
            "Nom": game.get("name"),
            "Date de sortie": game.get("released"),
            "Note Metacritic": game.get("metacritic"),
            "Note Utilisateur": game.get("rating"),
            "Nombre d'avis": game.get("ratings_count"),
            "Plateformes": ", ".join([platform["platform"]["name"] for platform in game.get("platforms", [])]),
            "Genres": ", ".join([genre["name"] for genre in game.get("genres", [])]),
            "Tags": ", ".join([tag["name"] for tag in game.get("tags", [])[:5]])  # Limite à 5 tags
        })
    return pd.DataFrame(games)

def main():
    # Nombre total de jeux à récupérer
    TOTAL_GAMES = 50000
    PAGE_SIZE = 40  # Nombre de jeux par page
    games_list = []

    # Pagination pour récupérer plusieurs pages
    for page in range(1, (TOTAL_GAMES // PAGE_SIZE) + 2):
        print(f"Récupération de la page {page}...")
        data = fetch_games(API_KEY, page=page, page_size=PAGE_SIZE)
        if data:
            df = parse_game_data(data)
            games_list.append(df)
        else:
            print("Impossible de récupérer plus de données.")
            break
        time.sleep(1)
        

    # Concaténer toutes les pages en un seul tableau
    full_df = pd.concat(games_list, ignore_index=True)
    print("Données récupérées avec succès !")

    # Affichage des 10 premières lignes
    print(full_df.head())

    # Sauvegarde en CSV pour analyse future
    full_df.to_csv("rawg_games_data.csv", index=False)
    print("Les données ont été sauvegardées dans 'rawg_games_data.csv'.")

if __name__ == "__main__":
    main()
