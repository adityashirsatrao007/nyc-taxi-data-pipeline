"""Load a parquet file into the warehouse target.

Used by the Airflow DAG. Kept small and dependency-light: uses duckdb
locally (or pandas + SQLAlchemy when configured).
"""

import os
import sys


def main():
    src = sys.argv[1]
    engine = os.getenv("WAREHOUSE_ENGINE", "duckdb")
    if engine == "duckdb":
        import duckdb

        con = duckdb.connect("/tmp/nyc_taxi/warehouse.duckdb")
        con.execute("CREATE OR REPLACE TABLE trips AS SELECT * FROM read_parquet(?)", [src])
        n = con.execute("SELECT COUNT(*) FROM trips").fetchone()[0]
        print(f"Loaded {n} rows into duckdb warehouse")
    else:
        import pandas as pd
        from sqlalchemy import create_engine

        df = pd.read_parquet(src)
        db = create_engine(engine)
        df.to_sql("trips", db, if_exists="replace", index=False)
        print(f"Loaded {len(df)} rows into {engine}")


if __name__ == "__main__":
    main()
