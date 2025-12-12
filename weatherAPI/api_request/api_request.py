import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_weather_data():
    # Fetch current weather data from Weatherstack API
    print("Fetching weather data...")
    try:
        api_key = os.environ.get("WEATHERSTACK_API_KEY")
        base_url = os.environ.get("WEATHERSTACK_BASE_URL")
        city = os.environ.get("WEATHERSTACK_CITY")
    
        params = {
            "access_key": api_key,
            "query": city
        }
        response = requests.get(base_url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None
   
def mock_data():
    return {
    "request": {
        "type": "City",
        "query": "New York, United States of America",
        "language": "en",
        "unit": "m"
    },
    "location": {
        "name": "New York",
        "country": "United States of America",
        "region": "New York",
        "lat": "40.714",
        "lon": "-74.006",
        "timezone_id": "America/New_York",
        "localtime": "2019-09-07 08:14",
        "localtime_epoch": 1567844040,
        "utc_offset": "-4.0"
    },
    "current": {
        "observation_time": "12:14 PM",
        "temperature": 13,
        "weather_code": 113,
        "weather_icons": [
            "https://assets.weatherstack.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png"
        ],
        "weather_descriptions": [
            "Sunny"
        ],
        "astro": {
            "sunrise": "06:31 AM",
            "sunset": "05:47 PM",
            "moonrise": "06:56 AM",
            "moonset": "06:47 PM",
            "moon_phase": "Waxing Crescent",
            "moon_illumination": 0
        },
        "air_quality": {
            "co": "468.05",
            "no2": "32.005",
            "o3": "55",
            "so2": "7.4",
            "pm2_5": "6.66",
            "pm10": "6.66",
            "us-epa-index": "1",
            "gb-defra-index": "1"
        },
        "wind_speed": 0,
        "wind_degree": 349,
        "wind_dir": "N",
        "pressure": 1010,
        "precip": 0,
        "humidity": 90,
        "cloudcover": 0,
        "feelslike": 13,
        "uv_index": 4,
        "visibility": 16
    }
}

if __name__ == "__main__":
    # Test the function
    # weather_data = fetch_weather_data()
    weather_data = mock_data()
    print(weather_data)