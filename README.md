<div align="center">

# NYC Taxi Data Pipeline

**End-to-end batch ETL — Airflow + dbt + BigQuery, raw → staging → marts.**

> **⚡ Impact:** daily batch ETL — Airflow-orchestrated dbt marts (raw → staging → marts) · 9 dbt data-quality tests on every load

Apache Airflow · dbt · BigQuery · DuckDB · Docker

[![CI](https://github.com/adityashirsatrao007/nyc-taxi-data-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/adityashirsatrao007/nyc-taxi-data-pipeline/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![dbt](https://img.shields.io/badge/dbt-v1.8-FF694B?logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

A daily batch ETL pipeline over NYC taxi trip data. **Airflow** orchestrates ingestion, **dbt** models the data through staging → intermediate → marts layers with automated data-quality tests, and results land in **BigQuery** for BI dashboards.

Runs fully locally with **DuckDB** (no cloud credentials required), so the pipeline can be demoed end-to-end with one command.

## Features

- **Orchestration** — Apache Airflow DAG with scheduled daily runs, retries, and idempotent backfills
- **Layered dbt modeling** — staging → intermediate → marts, one model per source
- **Data-quality tests** — not-null, uniqueness, relationships, accepted values
- **Dual warehouse support** — BigQuery (cloud) or DuckDB (local), switch via `profiles.yml`
- **BI ready** — marts feed Looker Studio / Metabase dashboards

## Architecture

```
NYC Taxi CSV ──▶ Airflow DAG
                    ├─ download ──▶ /tmp/raw
                    ├─ ingest   ──▶ warehouse (staging seed)
                    └─ trigger dbt ─▶ staging → intermediate → marts
                                       └──▶ Looker Studio / Metabase dashboards
```

## Quick start (local, no cloud needed)

```bash
cd nyc-taxi-data-pipeline

# Option A — everything via Docker Compose (Airflow + dbt + DuckDB)
docker compose up --build

# Option B — dbt project against DuckDB (fastest to demo)
python -m venv .venv && source .venv/bin/activate
pip install dbt-duckdb duckdb
cd dbt/nyc_taxi
dbt seed && dbt build
```

### To run against real BigQuery

```bash
pip install dbt-bigquery
cd dbt/nyc_taxi
dbt deps
dbt seed --target bigquery
dbt build --target bigquery
```

Set `BIGQUERY_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS` in your environment (or `profiles.yml`).

## dbt layer structure

| Layer | Purpose |
|-------|---------|
| `staging/` | Clean, type, and rename source data — one model per source |
| `marts/` | Business-facing aggregates (daily trips, revenue, top routes) |
| `tests/` | Not-null, uniqueness, relationships, accepted values |

## Project layout

```
dags/            Apache Airflow DAG (ingest + dbt trigger)
dbt/nyc_taxi/    dbt project — models, seeds, profiles, tests
scripts/         load helpers
docker-compose.yml  full local stack
```

## License

[MIT](LICENSE)

## Contributing

Contributions are welcome! For significant changes, please open an issue first to discuss the proposal.

1. Fork the repository and create a feature branch.
2. Make your changes (add tests where applicable).
3. Ensure the CI workflow passes.
4. Open a pull request with a clear description.

This project is released under the MIT License — see [`LICENSE`](LICENSE).
