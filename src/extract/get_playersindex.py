from nba_api.stats.endpoints import playerindex
import pandas as pd
from google.cloud import bigquery

def upload_to_bigquery(df, table_id, write_disposition="WRITE_TRUNCATE"):
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"✅ Dados enviados ao BigQuery: {table_id}")


def get_players_index(season="2025-26"):
    df = playerindex.PlayerIndex(
        season=season,
        league_id="00"
    ).get_data_frames()[0]

    return df[[
   "PERSON_ID",
   "PLAYER_LAST_NAME",
   "PLAYER_FIRST_NAME",
   "PLAYER_SLUG",
   "TEAM_ID",
   "TEAM_SLUG",
   "IS_DEFUNCT",
   "TEAM_CITY",
   "TEAM_NAME",
   "TEAM_ABBREVIATION",
   "JERSEY_NUMBER",
   "POSITION",
   "HEIGHT",
   "WEIGHT",
   "COLLEGE",
   "COUNTRY",
   "DRAFT_YEAR",
   "DRAFT_ROUND",
   "DRAFT_NUMBER",
   "ROSTER_STATUS",
   "PTS",
   "REB",
   "AST",
   "STATS_TIMEFRAME",
   "FROM_YEAR",
   "TO_YEAR"
    ]]


def full_get_player_index():
    df = get_players_index()

    project_id = "nba-project-478023"
    dataset = "nba_raw"
    table = "players_index"
    table_id = f"{project_id}.{dataset}.{table}"

    upload_to_bigquery(df, table_id)


if __name__ == "__main__":
    full_get_player_index()
