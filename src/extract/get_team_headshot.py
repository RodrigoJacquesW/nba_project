import requests
from pathlib import Path
from get_teams import get_teams_nba
import cairosvg

POSSIBLE_PATHS = [
    "global/L/logo.png",
    "global/D/logo.png",
    "primary/L/logo.png",
    "primary/D/logo.png",
    "global/L/logo.svg",
    "global/D/logo.svg",
    "primary/L/logo.svg",
    "primary/D/logo.svg",
]

def download_and_convert_logo(team_id, folder="data/headshots/teamsheadshot"):
    base = f"https://cdn.nba.com/logos/nba/{team_id}"
    output_path = Path(folder) / f"{team_id}.png"

    Path(folder).mkdir(parents=True, exist_ok=True)

    for path in POSSIBLE_PATHS:
        url = f"{base}/{path}"
        r = requests.get(url)

        if r.status_code == 200:
            print(f"✔ Logo encontrada: {url}")

            if url.endswith(".png"):
                with open(output_path, "wb") as f:
                    f.write(r.content)
                print(f"   → Salvo como PNG: {output_path}")
                return

       
            if url.endswith(".svg"):
                svg_temp = Path(folder) / f"{team_id}.svg"
                
                with open(svg_temp, "wb") as f:
                    f.write(r.content)

                cairosvg.svg2png(url=str(svg_temp), write_to=str(output_path))
                svg_temp.unlink()  
                
                print(f"   → Convertido SVG → PNG: {output_path}")
                return

    print(f"✘ Nenhum logo encontrado para ID {team_id}")


def download_all_team_logos():
    teams = get_teams_nba()
    team_ids = teams["id"].tolist()

    print(f"Baixando logos para {len(team_ids)} times...\n")

    for tid in team_ids:
        download_and_convert_logo(tid)


if __name__ == "__main__":
    download_all_team_logos()
