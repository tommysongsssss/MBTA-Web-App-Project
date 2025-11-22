import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com"

def get_json(url: str) -> dict:
    """Request a URL and return JSON response as a dictionary."""
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        return json.loads(data)

def get_lat_lng(place_name: str) -> tuple[str, str]:
    """Use Mapbox API to convert place name → (lat, lon)."""
    place_name = place_name.replace(" ", "%20")
    url = f"{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}"
    data = get_json(url)
    lon, lat = data["features"][0]["geometry"]["coordinates"]
    return str(lat), str(lon)

def get_nearest_station(lat: str, lon: str) -> tuple[str, bool]:
    """Use MBTA API to get nearest stop from coordinates."""
    url = (
        f"{MBTA_BASE_URL}/stops?"
        f"api_key={MBTA_API_KEY}"
        f"&filter[latitude]={lat}"
        f"&filter[longitude]={lon}"
        f"&sort=distance"
    )
    data = get_json(url)
    stop = data["data"][0]
    name = stop["attributes"]["name"]
    accessible = stop["attributes"]["wheelchair_boarding"] == 1
    return name, accessible

def find_stop_near(place_name: str) -> tuple[str, bool]:
    lat, lon = get_lat_lng(place_name)
    return get_nearest_station(lat, lon)

if __name__ == "__main__":
    print(find_stop_near("Boston Common"))
