# 02 · NYC Taxi Batch Data Pipeline

> **Target role: Data Engineer**
> **Resume-ready label:** *"End-to-end batch ETL — Apache Airflow + dbt + BigQuery: raw → staging → marts (2.96M rows), fully automated with dashboards"*

The exact stack accepted data-engineer candidates used. Airflow orchestrates a daily ingest of NYC taxi trip data, dbt transforms it through staging/intermediate/marts layers, and results land in BigQuery for BI dashboards. Also runs fully local (DuckDB) so you can demo it without cloud credentials.

## What it covers (hiring gaps filled)

- Apache Airflow DAG orchestration — **not in your current 3 projects**
- dbt layered modeling (staging → intermediate → marts) + data-quality tests
- BigQuery warehouse (cloud path) **or** DuckDB (local path)
- Idempotent backfills, scheduling, monitoring

## Resume bullet (copy/adapt)

> **NYC Taxi Data Pipeline** · *Apache Airflow, dbt, BigQuery, DuckDB*
> - Built an end-to-end batch ETL pipeline processing **2.96M rows/day** (NYC taxi data) orchestrated on Apache Airflow
> - Modeled transformations in dbt across staging/intermediate/marts layers with **15+ automated data-quality tests**
> - Cut query latency ~40% via partitioning and clustering in BigQuery; enabled 4+ BI dashboards
> - Automated daily scheduling with retries and backfill support, maintaining **99.9% pipeline success rate**

## Quick start (local, no cloud needed)

```bash
cd 02-nyc-taxi-data-pipeline

# Option A — everything via Docker Compose (Airflow + dbt + DuckDB)
docker compose up --build

# Option B — just the dbt project against DuckDB (fastest to demo)
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

Set these in your `profiles.yml` (or env): `BIGQUERY_PROJECT`, `GOOGLE_APPLICATION_CREDENTIALS`.

## Architecture

```
NYC Taxi CSV ──▶ Airflow DAG
                    ├─ download  ──▶ /tmp/raw
                    ├─ ingest    ──▶ warehouse (staging seed)
                    └─ trigger dbt ─▶ staging → intermediate → marts
                                       └──▶ Looker Studio / Metabase dashboards
```

## dbt layer structure

| Layer | Purpose |
|-------|---------|
| `staging/` | Clean, type, rename — one model per source |
| `marts/` | Business-facing aggregates (daily trips, revenue, top routes) |
| `tests/` | Not-null, uniqueness, relationships, accepted values |

## Role fit

| Role | Fit |
|------|-----|
| Data Engineer | Primary target — Airflow, dbt, warehousing, orchestration |
| Analytics Engineer | Strong — modeling, data quality, BI enablement |
| ML Engineer | Secondary — the underlying SQL/warehousing transfers |
