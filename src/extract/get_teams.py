from nba_api.stats.static import teams
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


def get_teams_nba():
    nba_teams = teams.get_teams()
    df = pd.DataFrame(nba_teams)
    df = df.sort_values("full_name").reset_index(drop=True)
    return df


def full_get_teams():
    df = get_teams_nba()

    project_id = "nba-project-478023"
    dataset = "nba_raw"
    table = "teams"
    table_id = f"{project_id}.{dataset}.{table}"

    upload_to_bigquery(df, table_id)


if __name__ == "__main__":
    full_get_teams()
