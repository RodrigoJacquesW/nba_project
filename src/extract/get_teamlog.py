from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import teams
import pandas as pd
from google.cloud import bigquery 
import time

def upload_to_bigquery (df,table_id, write_disposition = "WRITE_TRUNCATE"):

    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition = write_disposition,
        autodetect = True
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()
    print(f"✅ Dados enviados ao BigQuery: {table_id}")

def get_all_teams_gamelogs(season="2025-26"):
    print(f"Coletando todos os gamelogs da temporada {season}...")

    logs = leaguegamelog.LeagueGameLog(
        season=season,
        season_type_all_star="Regular Season"
    ).get_data_frames()[0]

    
    return logs

def full_team_gamelog():
    df = get_all_teams_gamelogs()

    project_id = "nba-project-478023"
    dataset = "nba_raw"
    table = "teamlog"
    table_id = f"{project_id}.{dataset}.{table}"

    upload_to_bigquery(df, table_id)


if __name__ == "__main__":
    full_team_gamelog()
