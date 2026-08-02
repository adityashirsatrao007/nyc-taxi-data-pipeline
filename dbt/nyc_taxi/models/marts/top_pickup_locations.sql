{{ config(materialized="table", schema="marts") }}

-- Top pickup locations by revenue.
with trips as (
    select * from {{ ref("stg_trips") }}
),

top_locations as (
    select
        pickup_location_id,
        count(*) as trip_count,
        round(sum(total_amount), 2) as total_revenue,
        round(avg(tip_amount), 2) as avg_tip
    from trips
    group by 1
    order by total_revenue desc
    limit 20
)

select * from top_locations
