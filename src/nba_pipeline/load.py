"""Load DataFrames into the BigQuery raw dataset."""

from datetime import datetime, timezone

import pandas as pd
from google.cloud import bigquery

from .config import Settings


def load_raw(df: pd.DataFrame, table: str, settings: Settings) -> None:
    """Full refresh of one raw table (WRITE_TRUNCATE), adding an ingestion timestamp."""
    client = bigquery.Client(project=settings.gcp_project_id, location=settings.bq_location)

    dataset_ref = bigquery.Dataset(f"{settings.gcp_project_id}.{settings.raw_dataset}")
    dataset_ref.location = settings.bq_location
    client.create_dataset(dataset_ref, exists_ok=True)

    df = df.copy()
    df["_ingested_at"] = datetime.now(timezone.utc)

    job = client.load_table_from_dataframe(
        df,
        settings.table_id(table),
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True),
    )
    job.result()
    print(f"  loaded {len(df):>6,} rows -> {settings.table_id(table)}")
