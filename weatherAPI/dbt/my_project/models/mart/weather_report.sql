{{ config(
    materialized='table', 
    unique_key='id'
) }}

-- Because of ref, dbt knows it must finish building 
--stg_weather_data successfully before it tries to build weather_report.
select * from {{ ref('stg_weather_data') }}