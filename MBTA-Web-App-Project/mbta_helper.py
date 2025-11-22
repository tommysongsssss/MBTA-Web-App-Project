import os
import json
import urllib.request
import urllib.parse
from typing import Tuple, List, Set

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)


def get_lat_lng(place_name: str) -> Tuple[float, float]:
    if not MAPBOX_TOKEN:
        raise RuntimeError("MAPBOX_TOKEN is not set in .env")

    encoded = urllib.parse.quote(place_name)
    url = f"{MAPBOX_BASE_URL}/{encoded}.json?access_token={MAPBOX_TOKEN}"
    data = get_json(url)

    if not data.get("features"):
        raise ValueError("No location results from Mapbox")

    lon, lat = data["features"][0]["geometry"]["coordinates"]
    return float(lat), float(lon)


def _get_lines_for_stop(stop_id: str) -> List[str]:
    if not MBTA_API_KEY:
        raise RuntimeError("MBTA_API_KEY is not set in .env")

    url = (
        f"{MBTA_BASE_URL}/routes"
        f"?api_key={MBTA_API_KEY}"
        f"&filter[stop]={stop_id}"
    )
    data = get_json(url)

    lines: Set[str] = set()

    for route in data.get("data", []):
        rid = route.get("id", "")

        if rid.startswith("Red"):
            lines.add("red")
        elif rid.startswith("Orange"):
            lines.add("orange")
        elif rid.startswith("Green"):
            lines.add("green")
        elif rid.startswith("Blue"):
            lines.add("blue")
        elif rid.startswith("Silver"):
            lines.add("silver")

    return sorted(lines)


def get_nearest_station(latitude: float, longitude: float):
    if not MBTA_API_KEY:
        raise RuntimeError("MBTA_API_KEY is missing")

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
    stop_id = stop["id"]
    name = stop["attributes"]["name"]
    accessible = stop["attributes"]["wheelchair_boarding"] == 1

    try:
        lines = _get_lines_for_stop(stop_id)
    except:
        lines = []

    return name, accessible, lines, stop_id


def find_stop_near(place: str):
    lat, lon = get_lat_lng(place)
    name, accessible, lines, _ = get_nearest_station(lat, lon)
    return name, accessible, lat, lon, lines


def find_stop_near_coords(lat: float, lon: float):
    name, accessible, lines, _ = get_nearest_station(lat, lon)
    return name, accessible, lat, lon, lines
