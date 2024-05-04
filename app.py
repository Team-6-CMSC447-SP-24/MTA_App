from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *
from credentials import google_key

isLoggedIn = False
currentUser = None

app = Flask(__name__)
@app.context_processor
def inject_user(): # Allows for passing in login status for all pages
    return dict(isLoggedIn=isLoggedIn, currentUser=currentUser)

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

    rtVehicles = getRealTimeVehiclePositions()
    for vehicle in rtVehicles:
        if int(vehicle.tripId) == int(id):
            thisVehicle = vehicle
    lat = thisVehicle.latitude
    long = thisVehicle.longitude

    return render_template('tripupdate.html', stops=theseStops, vehicleLat=lat, vehicleLong=long, gKey=google_key)

@app.route('/<string:t_stop>/searchstops', methods=('GET', 'POST'))
def search(t_stop):
    rtVehicles = searchStopName(t_stop, getRealTimeTripUpdates(), getRealTimeVehiclePositions())
    vehiclesTable = ParseVehicles(rtVehicles)
    return render_template('index.html', vehicles=vehiclesTable)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global currentUser
    global isLoggedIn
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not findUser(username):
            error = 'Invalid user. Please try again.'
        elif not isValidLogin(username, password):
            error = 'Invalid password.'
        else:
            isLoggedIn = True
            currentUser = username
            print(f"[LOGIN] Current user: {currentUser}")
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    global isLoggedIn
    global currentUser
    isLoggedIn = False
    currentUser = None
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
