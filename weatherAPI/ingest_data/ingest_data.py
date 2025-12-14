import sys
import os

# Add parent directory to Python's module search path
# Why? Python only searches the script's directory by default, not sibling directories.
# 
# How it works:
# 1. __file__ = path to this script (ingest_data.py)
# 2. os.path.abspath(__file__) = absolute path to this script
# 3. os.path.dirname(...) first call = gets ingest_data directory
# 4. os.path.dirname(...) second call = gets weatherAPI directory (parent)
# 5. sys.path.insert(0, ...) = adds weatherAPI to Python's search path at position 0 (highest priority)
#
# Result: Python can now find and import from api_request folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_request.api_request import mock_data
from psycopg2 import connect
def postgres_connection():
    try:
        # To use docker's service and its port
        conn = connect(
            host="db",
            port="5432",
            user="postgres",
            password="postgres",
            dbname="db"
        )
        print("Postgres connection successful",conn)
        return conn
    except Exception as e:
        print(f"Error while connecting to Postgres: {e}")
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        # Few comments for understanding postgres sql
        # serial -> similar to identity column in sql server
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.weather(
                id SERIAL PRIMARY KEY,
                city text,
                temperature Float,
                weather_description text,
                wind_speed Float,
                humidity Int,
                time Timestamp,
                inserted_at Timestamp,
                utc_offset Text
            );
        """)
        conn.commit()
        print("Weather table created successfully")
    except Exception as e:
        print(f"Error while creating table: {e}")

def ingest_data(conn,data):
    try:
        current = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dev.weather(
            city, 
            temperature, 
            weather_description, 
            wind_speed, 
            humidity, 
            time, 
            inserted_at, 
            utc_offset
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s);
            """, 
            (
            location['name'], 
            current['temperature'], 
            current['weather_descriptions'][0], 
            current['wind_speed'], 
            current['humidity'], 
            location['localtime'], 
            location['utc_offset']
            )
        )
        conn.commit()
        print("Data ingested successfully")
    except Exception as e:
        print(f"Error while ingesting data to postgres: {e}")


def main():
    conn = None
    try:
        data = mock_data()
        conn = postgres_connection()
        if conn:
            create_table(conn)
            ingest_data(conn, data)
    except Exception as e:
        print(f"Error from run_weather_ingestion: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()

