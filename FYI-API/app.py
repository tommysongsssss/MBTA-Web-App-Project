from flask import Flask, render_template, request
from weather import find_temp

app = Flask(__name__)


# Home route
@app.route("/")
def homepage():
    return "This is the homepage!"


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name=None):
    if name:
        return f'Hello, {name}!'
    return "Hello from the /hello route!"


@app.route("/square")
@app.route("/square/<int:number>")
def square(number=None):
    if number: 
        return str(number ** 2)
    return "No number provided"


@app.route('/weather/<city>')
def show_temp(city):
    """Display the current temperature for a given city."""
    temperature = find_temp(city)
    return f'The current temperature in {city} is {temperature}°F'


# get just display the info
@app.get('/weather')
def weather_no_city():
    return render_template('weather-form.html')


# post allow user to type in the info
@app.post('/weather')
def weather_with_city():
    city = request.form.get('city')
    # print(city)
    if city:
        temperature = find_temp(city)
        return f'The current temperature in <strong>{city}<strong> is <span style=\"color:red"> {temperature}°F<span>.'
        # return redirect(url_for('show_temp', city=city))
    return "No city provided"

@app.post("/weather")
def weather_with_city():
    city = request.form.get("city")

    if not city:
        # No city submitted – re-render form with an error
        return render_template(
            "weather-form.html",
            error="Please enter a city name."
        )

    try:
        temperature = find_temp(city)
        return render_template(
            "weather-form.html",
            city=city,
            temperature=temperature,
            error=None,
        )
    except Exception as e:
        # Very simple error handling (invalid API key / bad city / network, etc.)
        return render_template(
            "weather-form.html",
            error=f"Could not get weather data: {e}"
        )



if __name__ == "__main__":
    app.run(debug=True)