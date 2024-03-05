from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *

def ParseVehicles(currentVehicles: list[Vehicle]) -> list[dict[str, str]]:
    tableInfo = []
    for vehicle in currentVehicles:
        thisId = vehicle.id
        thisRouteName = getRouteName(vehicle.routeId)
        tableInfo.append({'id': thisId, 'name': thisRouteName})
    return tableInfo

rtVehicles = getRealTimeVehiclePositions()
# showAllVehicles(rtVehicles)
vehiclesTable = ParseVehicles(rtVehicles)
# rtTrips = getRealTimeTripUpdates()
# showAllTrips(rtTrips)



app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', vehicles=vehiclesTable)

if __name__ == "__main__":
    app.run(debug=True)
    
