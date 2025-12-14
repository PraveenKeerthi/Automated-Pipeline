create user airflow with password 'airflow';
create database airflow_db owner airflow;
-- The initialization script does NOT run again
-- The script only runs once when 
-- the data directory is completely empty (first-time setup).