import os
import json
import urllib.request
import urllib.parse
from typing import Tuple

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com"


def get_json(url: str) -> dict:
    """Make a request to the given URL and return JSON response."""
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


def get_lat_lng(place_name: str) -> Tuple[float, float]:
    """
    Given a place name, return (lat, lon) as floats using Mapbox Geocoding API.
    """
    encoded_place = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{encoded_place}.json?access_token={MAPBOX_TOKEN}"
    data = get_json(url)

    if not data.get("features"):
        raise ValueError("No location results from Mapbox")

    coords = data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
    lon, lat = coords[0], coords[1]
    return float(lat), float(lon)


def get_nearest_station(latitude: float, longitude: float) -> Tuple[str, bool]:
    """
    Given latitude and longitude, return (station_name, wheelchair_accessible).
    """
    url = (
        f"{MBTA_BASE_URL}/stops"
        f"?api_key={MBTA_API_KEY}"
        f"&filter[latitude]={latitude}"
        f"&filter[longitude]={longitude}"
        f"&sort=distance"
    )

    data = get_json(url)

    if not data.get("data"):
        raise ValueError("No nearby MBTA stops found")

    stop = data["data"][0]
    name = stop["attributes"]["name"]
    accessible = stop["attributes"]["wheelchair_boarding"] == 1
    return name, accessible


def find_stop_near(place_name: str) -> Tuple[str, bool, float, float]:
    """
    Given a place name, return (station_name, accessible, lat, lon).
    """
    lat, lon = get_lat_lng(place_name)
    name, accessible = get_nearest_station(lat, lon)
    return name, accessible, lat, lon


def find_stop_near_coords(latitude: float, longitude: float) -> Tuple[str, bool, float, float]:
    """
    Given coordinates, return (station_name, accessible, lat, lon).
    """
    name, accessible = get_nearest_station(latitude, longitude)
    return name, accessible, float(latitude), float(longitude)


def main():
    # Quick manual test from terminal
    place = "Fenway Park, Boston, MA"
    station, accessible, lat, lon = find_stop_near(place)
    print(place, "->", station, accessible, lat, lon)


if __name__ == "__main__":
    main()
