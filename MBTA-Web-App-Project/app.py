from flask import Flask, render_template, request, redirect, url_for
from mbta_helper import find_stop_near

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place_name")
        if place:
            return redirect(url_for("nearest_mbta", place_name=place))
        return redirect(url_for("error"))
    return render_template("index.html")

@app.route("/nearest_mbta")
def nearest_mbta():
    place = request.args.get("place_name")
    if not place:
        return redirect(url_for("error"))

    try:
        station, accessible = find_stop_near(place)
        return render_template(
            "mbta_station.html",
            place=place,
            station_name=station,
            wheelchair_accessible=accessible
        )
    except Exception as e:
        print("ERROR:", e)
        return redirect(url_for("error"))

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
