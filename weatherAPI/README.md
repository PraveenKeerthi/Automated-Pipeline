# Weather API Project

This project fetches weather data from the Weatherstack API and is designed to be integrated into an Airflow pipeline.

## Prerequisites

- Python 3.x
- Weatherstack API key (get one free at [weatherstack.com](https://weatherstack.com))

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd weatherAPI
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```env
WEATHERSTACK_BASE_URL=http://api.weatherstack.com/current
WEATHERSTACK_API_KEY=your_api_key_here
WEATHERSTACK_CITY=New York
```

**Important:**

- Replace `your_api_key_here` with your actual Weatherstack API key
- You can change `WEATHERSTACK_CITY` to any city you want to track
- **Never commit the `.env` file to Git** - it contains sensitive API credentials

### 6. Run the Application

```bash
python api-request/api-request.py
```

## Project Structure

```
weatherAPI/
├── api-request/
│   └── api-request.py    # Main script to fetch weather data
├── .env                   # Environment variables (not tracked in Git)
├── .gitignore            # Git ignore file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Environment Variables

| Variable                | Description                    | Example                               |
| ----------------------- | ------------------------------ | ------------------------------------- |
| `WEATHERSTACK_BASE_URL` | Base URL for Weatherstack API  | `http://api.weatherstack.com/current` |
| `WEATHERSTACK_API_KEY`  | Your Weatherstack API key      | `abc123def456`                        |
| `WEATHERSTACK_CITY`     | City to fetch weather data for | `New York`                            |

## Usage

The `fetch_weather_data()` function in `api-request.py` fetches current weather data from the Weatherstack API. The response includes:

- Location information (city, country, coordinates)
- Current weather conditions (temperature, description, wind speed, etc.)
- Astronomical data (sunrise, sunset, moon phase)
- Air quality metrics

## Integration with Airflow

This script is designed to be used as part of an Airflow DAG. You can integrate it using a `PythonOperator`:

```python
from airflow.operators.python import PythonOperator
from api_request import fetch_weather_data

fetch_weather_task = PythonOperator(
    task_id='fetch_weather',
    python_callable=fetch_weather_data,
    dag=dag
)
```

## Troubleshooting

- **API Key Error**: Ensure your `.env` file exists and contains a valid `WEATHERSTACK_API_KEY`
- **Module Not Found**: Make sure you've activated the virtual environment and installed dependencies
- **Connection Error**: Check your internet connection and verify the API endpoint is accessible

## Security Notes

- The `.env` file is excluded from Git via `.gitignore`
- Never share your API key publicly
- For production deployments, use secure secret management (e.g., Airflow Variables, AWS Secrets Manager)
