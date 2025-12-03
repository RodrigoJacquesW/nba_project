from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import teams
from nba_api.stats.static import players
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


def get_players_gamelog(season ="2025-26"):
    player_list = players.get_players()
    players_ids = [p["id"] for p in player_list if p["is_active"]]
    all_logs=[]

    for pid in players_ids:
        log = playergamelog.PlayerGameLog(
            player_id = pid,   
            season=season,
            season_type_all_star="Regular Season"
        ).get_data_frames()[0]

        if not log.empty:
            all_logs.append(log)

        time.sleep(0.6) 

    df = pd.concat(all_logs, ignore_index=True)
    return df

def full_get_gamelog():
    df = get_players_gamelog()

    project_id = "nba-project-478023"
    dataset = "nba_raw"
    table = "gamelog"
    table_id = f"{project_id}.{dataset}.{table}"

    upload_to_bigquery(df, table_id)


if __name__ == "__main__":
    full_get_gamelog()



