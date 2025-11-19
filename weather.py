# BUild a terminal based weatehr checker
# It should ask user to enter a city, and how the current temperature

import json
import os
import urllib.request


from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv("OPENWEATHER_API_KEY")


def find_temp(city):
    """Return the current temperature for a given city, everything that involves API"""
    country_code = "us"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&APPID={APIKEY}&units=imperial"

    # print(url)

    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        weather_data = json.loads(response_text)
        return weather_data['main']['temp']


def app():
    """Create the dialog in terminal to ask user for city 
    name, and display the current temperature"""
    city = input("Please enter a city name (in US): ")
    temp = find_temp(city)
    print(f'The current temperature in {city} is {temp}°F')

def main():
    print(find_temp("Wellesley"))
    #app()


if __name__ == "__main__":
    app()