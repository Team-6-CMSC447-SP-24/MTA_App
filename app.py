from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *


app = Flask(__name__)
@app.route('/')
def index():
    rtVehicles = getRealTimeVehiclePositions()
    vehiclesTable = ParseVehicles(rtVehicles)
    return render_template('index.html', vehicles=vehiclesTable)

@app.route('/<int:id>/tripupdate', methods=('GET', 'POST'))
def tripupdate(id):
    rtTrips = getRealTimeTripUpdates()
    thisTrip = None
    theseStops = []
    for trip in rtTrips:
        if int(trip.tripId) == int(id):
            thisTrip = trip
    theseStops= ParseStops(thisTrip)
    
    return render_template('tripupdate.html', stops=theseStops)
    

if __name__ == "__main__":
    app.run(debug=True)
    # showAllVehicles(rtVehicles)
    #showAllTrips(rtTrips)
