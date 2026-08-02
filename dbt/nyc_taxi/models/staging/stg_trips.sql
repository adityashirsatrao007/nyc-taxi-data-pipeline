{{ config(materialized="view", schema="staging") }}

-- Staging layer: clean, type, and rename raw trips.
with source as (
    select * from {{ ref("trips") }}
),

renamed as (
    select
        vendorid as vendor_id,
        pickup_datetime,
        dropoff_datetime,
        passenger_count,
        trip_distance,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        improvement_surcharge,
        total_amount,
        payment_type,
        ratecodeid as rate_code_id,
        pulocationid as pickup_location_id,
        dolocationid as dropoff_location_id
    from source
),

cleaned as (
    select *
    from renamed
    where
        pickup_datetime is not null
        and trip_distance >= 0
        and passenger_count >= 0
        and total_amount >= 0
)

select * from cleaned
