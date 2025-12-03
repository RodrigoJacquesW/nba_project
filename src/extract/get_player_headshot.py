import requests
from pathlib import Path
from get_players import get_players_nba

def download_headshot(player_id, folder="data/headshots"):
    url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    save_path = Path(folder) / f"{player_id}.png"
    
    response = requests.get(url)

    if response.status_code == 200:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"✔ Foto salva: {save_path}")
    else:
        print(f"✘ Foto não encontrada para ID {player_id}")


def download_all_headshots():
    players = get_players_nba()

    if hasattr(players, "iterrows"): 
        players = players[players["is_active"] == True]
        player_ids = players["id"].tolist()
    else:
        raise ValueError("Formato inesperado retornado por get_players_nba")

    print(f"Baixando fotos para {len(player_ids)} jogadores ativos...\n")

    for pid in player_ids:
        download_headshot(pid) 


if __name__ == "__main__":
    download_all_headshots()
