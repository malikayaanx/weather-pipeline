import json
from datetime import date
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / str(date.today())

API_URL = "https://api.open-meteo.com/v1/forecast"
CITIES = {
    "vadodara": (22.31, 73.18),
    "mumbai": (19.08, 72.88),
    "delhi": (28.61, 77.21),
}


def fetch_city(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "past_days": 7,
        "timezone": "auto",
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for city, (lat, lon) in CITIES.items():
        data = fetch_city(lat, lon)
        file_path = RAW_DIR / f"{city}.json"
        file_path.write_text(json.dumps(data, indent=2))
        print(f"Saved {file_path}")


if __name__ == "__main__":
    main()