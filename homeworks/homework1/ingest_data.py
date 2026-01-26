#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


def ingest_csv(url_or_path: str, engine, target_table: str, chunksize: int, dtype=None, parse_dates=None):
    df_iter = pd.read_csv(
        url_or_path,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    first_chunk = next(df_iter)

    # Create table using schema inferred from first chunk
    first_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace", index=False)
    print(f"Table {target_table} created")

    # Insert first chunk
    first_chunk.to_sql(name=target_table, con=engine, if_exists="append", index=False)
    print(f"Inserted first chunk: {len(first_chunk)}")

    # Insert remaining chunks
    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append", index=False)
        print(f"Inserted chunk: {len(df_chunk)}")

    print(f"Done ingesting CSV into {target_table}")


def ingest_parquet(path: str, engine, target_table: str):
    df = pd.read_parquet(path)

    # Replace table and load all at once (usually fine for monthly parquet)
    df.to_sql(name=target_table, con=engine, if_exists="replace", index=False)
    print(f"Done ingesting Parquet into {target_table} ({len(df)} rows)")


@click.command()
@click.option("--pg-user", default="root")
@click.option("--pg-pass", default="root")
@click.option("--pg-host", default="localhost")
@click.option("--pg-port", default="5432")
@click.option("--pg-db", default="ny_taxi")
@click.option("--source", required=True, help="Path or URL to data file (.csv/.csv.gz/.parquet)")
@click.option("--target-table", required=True, help="Target table name in Postgres")
@click.option("--chunksize", default=100000, type=int, help="Chunk size for CSV ingestion")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, source, target_table, chunksize):
    engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

    source_lower = source.lower()

    # For parquet: no dtype needed; schema is embedded
    if source_lower.endswith(".parquet"):
        ingest_parquet(source, engine, target_table)
        return

    # For CSVs: you can keep it generic, or optionally specialize when it's yellow taxi
    # Keeping generic here is fine for zones CSV and most tasks.
    ingest_csv(
        source,
        engine,
        target_table,
        chunksize=chunksize,
        dtype=None,
        parse_dates=None
    )


if __name__ == "__main__":
    main()


