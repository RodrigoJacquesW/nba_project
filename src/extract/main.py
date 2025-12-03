import subprocess
from get_gamelist import full_load_games
from get_gamelogs import full_get_gamelog
from get_players import full_get_player
from get_teamlog import full_team_gamelog
from get_teams import full_get_teams
from get_team_headshot import download_all_team_logos
from get_player_headshot import download_all_headshots

def main():
    print("Baixando players...")
    full_get_player()

    print("Baixando teams...")
    full_get_teams()

    print("Baixando lista de jogos...")
    full_load_games()

    print("Baixando game logs dos jogadores...")
    full_get_gamelog()

    print("Baixando game logs dos times...")
    full_team_gamelog()

    print("Baixando headshots dos jogadores..")
    download_all_headshots()

    print("Baixando headshots dos times..")
    download_all_team_logos()

    print("\nRodando Dataform (todas as camadas)...")
    subprocess.run(["dataform", "run"], check=True)

    print("\nPipeline finalizada com sucesso!")

if __name__ == "__main__":
    main()
