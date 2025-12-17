-- unique key is used to identify each row in the table
{{ config(
    materialized='table',
    unique_key='id'
) }}

with source as 
(
    select * from {{ source('weather', 'weather') }}
)

select
    id,
    city,
    temperature,
    weather_description,
    wind_speed,
    humidity,
    time,
    (inserted_at + (utc_offset || ' hours')::interval) as local_time
from source
