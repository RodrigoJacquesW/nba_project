import requests
from pathlib import Path
from get_teams import get_teams_nba

POSSIBLE_PATHS = [
    "global/L/logo.png",
    "global/D/logo.png",
    "global/L/logo.svg",
    "global/D/logo.svg",
    "primary/L/logo.png",
    "primary/D/logo.png",
    "primary/L/logo.svg",
    "primary/D/logo.svg",
]

def download_team_logo(team_id, folder="data/headshots/teamsheadshot"):
    base = f"https://cdn.nba.com/logos/nba/{team_id}"
    save_path = Path(folder) / f"{team_id}.png"

    Path(folder).mkdir(parents=True, exist_ok=True)

    for path in POSSIBLE_PATHS:
        url = f"{base}/{path}"
        r = requests.get(url)

        if r.status_code == 200:
            ext = ".svg" if url.endswith(".svg") else ".png"
            save_path = Path(folder) / f"{team_id}{ext}"

            with open(save_path, "wb") as f:
                f.write(r.content)

            print(f"✔ Logo encontrada ({ext}): {url}")
            return

    print(f"✘ Nenhum logo encontrado para ID {team_id}")


def download_all_team_logos():
    teams = get_teams_nba()
    team_ids = teams["id"].tolist()

    print(f"Baixando logos para {len(team_ids)} times...\n")

    for tid in team_ids:
        download_team_logo(tid)


if __name__ == "__main__":
    download_all_team_logos()
