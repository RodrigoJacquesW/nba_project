from nba_api.stats.endpoints import LeagueGameLog
import pandas as pd
from google.cloud import bigquery

def upload_to_bigquery(df, table_id, write_disposition="WRITE_TRUNCATE"):

    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
        autodetect=True
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    )

    job.result()
    print(f"✅ Dados enviados ao BigQuery: {table_id}")


def get_unique_games(season="2025-26"):

    df = LeagueGameLog(
        season=season,
        season_type_all_star="Regular Season"
    ).get_data_frames()[0]


    df_unique = df.drop_duplicates(subset="GAME_ID")


    df_unique = df_unique.sort_values("GAME_DATE")

    return df_unique


def full_load_games():
    df_unique = get_unique_games("2025-26")

    table_id = "nba-project-478023.nba_raw.games_unique"

    upload_to_bigquery(df_unique, table_id)


if __name__ == "__main__":
    full_load_games()
