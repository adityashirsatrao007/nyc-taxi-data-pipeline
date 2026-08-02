{{ config(materialized="table", schema="marts") }}

-- Daily trip aggregates by pickup day.
with trips as (
    select * from {{ ref("stg_trips") }}
),

daily as (
    select
        date(pickup_datetime) as trip_date,
        count(*) as trip_count,
        count(distinct pickup_location_id) as unique_pickup_locations,
        round(sum(total_amount), 2) as total_revenue,
        round(sum(tip_amount), 2) as total_tips,
        round(avg(trip_distance), 2) as avg_trip_distance,
        round(avg(total_amount), 2) as avg_fare
    from trips
    group by 1
)

select * from daily
