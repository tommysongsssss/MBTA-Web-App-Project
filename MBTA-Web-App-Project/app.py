from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from typing import Optional

from mbta_helper import find_stop_near, find_stop_near_coords

# Load environment variables
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
HOLIDAYS_API_KEY = os.getenv("HOLIDAYS_API_KEY")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

app = Flask(__name__)


# ------------------ Helper functions: weather, holidays, static map ------------------ #

def get_weather(city: str = "Boston") -> str:
    if not OPENWEATHER_API_KEY:
        return "Weather: API key missing"
    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        return f"{temp:.1f}°C, {desc}"
    except Exception:
        return "Weather data not available"


def get_today_holiday(country: str = "US") -> str:
    if not HOLIDAYS_API_KEY:
        return "Holiday: API key missing"

    today = datetime.now()
    try:
        url = (
            "https://holidays.abstractapi.com/v1/"
            f"?api_key={HOLIDAYS_API_KEY}"
            f"&country={country}"
            f"&year={today.year}"
            f"&month={today.month}"
            f"&day={today.day}"
        )
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        holidays = resp.json()

        if isinstance(holidays, list) and len(holidays) > 0:
            name = holidays[0].get("name", "a holiday")
            return f"Today is {name}"
        else:
            return "Today is not a holiday"
    except Exception:
        return "Holiday data not available"


def build_static_map_url(lat: float, lng: float) -> Optional[str]:
    if not MAPBOX_TOKEN:
        return None

    lon = lng
    zoom = 14
    width, height = 600, 300
    marker = f"pin-l-marker+FF7F00({lon},{lat})"

    url = (
        "https://api.mapbox.com/styles/v1/mapbox/light-v11/static/"
        f"{marker}/{lon},{lat},{zoom},0/{width}x{height}"
        f"?access_token={MAPBOX_TOKEN}"
    )
    return url


def get_common_header_context():
    date_today = datetime.now().strftime("%A, %B %d, %Y")
    weather_today = get_weather()
    holiday_today = get_today_holiday()
    return dict(
        date_today=date_today,
        weather_today=weather_today,
        holiday_today=holiday_today,
    )


# ------------------------------ Routes -------------------------------- #

@app.route("/", methods=["GET", "POST"])
def index():
    context = get_common_header_context()

    if request.method == "POST":
        place = (request.form.get("place_name") or "").strip()

        lat_str = (request.form.get("lat") or "").strip()
        lng_str = (request.form.get("lng") or "").strip()

        if lat_str and lng_str:
            return redirect(url_for("nearest_mbta_coords", lat=lat_str, lng=lng_str))

        if place:
            return redirect(url_for("nearest_mbta", place_name=place))

        return redirect(url_for("error"))

    return render_template("index.html", **context)


@app.route("/nearest_mbta")
def nearest_mbta():
    place = request.args.get("place_name", "").strip()
    if not place:
        return redirect(url_for("error"))

    try:
        station_name, accessible, lat, lng, lines = find_stop_near(place)
        static_map_url = build_static_map_url(lat, lng)

        context = get_common_header_context()
        context.update(
            place=place,
            station_name=station_name,
            wheelchair_accessible=accessible,
            static_map_url=static_map_url,
            lines=lines,
        )
        return render_template("mbta_station.html", **context)

    except Exception as e:
        print("Error in /nearest_mbta:", e)
        return redirect(url_for("error"))


@app.route("/nearest_mbta_coords")
def nearest_mbta_coords():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if not lat or not lng:
        return redirect(url_for("error"))

    try:
        lat_float = float(lat)
        lng_float = float(lng)

        station_name, accessible, lat2, lng2, lines = find_stop_near_coords(lat_float, lng_float)
        static_map_url = build_static_map_url(lat2, lng2)

        context = get_common_header_context()
        context.update(
            place="Your current location",
            station_name=station_name,
            wheelchair_accessible=accessible,
            static_map_url=static_map_url,
            lines=lines,
        )
        return render_template("mbta_station.html", **context)

    except Exception as e:
        print("Error in /nearest_mbta_coords:", e)
        return redirect(url_for("error"))


@app.route("/error")
def error():
    context = get_common_header_context()
    return render_template("error.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
