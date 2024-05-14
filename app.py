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

@app.route('/search/<string:t_stop>', methods=('GET', 'POST'))
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

@app.route('/logout', methods=['GET'])
def logout():
    global isLoggedIn
    global currentUser
    isLoggedIn = False
    currentUser = None
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    global isLoggedIn
    global currentUser
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif findUser(username):
            error = 'User already exists.'
        else:
            isLoggedIn = True
            currentUser = username
            print(registerUser(username, password))
            return redirect(url_for('index'))
    
    return render_template('register.html', error=error)

@app.route('/<int:id>/addfavorite')
def addfavorite(id):
    routeId = getRouteFromTripId(id)
    routeName = getRouteName(routeId)
    addFavoriteRoute(currentUser, routeName, routeId)

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT * FROM favorites"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

    return redirect(url_for('index'))
@app.route('/<string:user>/favorites')
def favorites(user: str):
    if isLoggedIn:
        userFavorites = getAllFavorites(user)
        return render_template('favorites.html', favorites=userFavorites)
    else:
        print(f"Not logged in.")
        return redirect(url_for('index'))

@app.route('/<int:id>/route', methods=('GET', 'POST'))
def route(id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT trip_id FROM trips WHERE route_id = ?"
    cursor.execute(query, (id,))
    rows = cursor.fetchall()

    query = "SELECT route_long_name FROM routes WHERE route_id = ?"
    cursor.execute(query, (id,))
    routeName = cursor.fetchall()
    routeName = routeName[0][0]
    conn.close()

    rtTrips = getRealTimeTripUpdates()
    thisTrip = None
    theseStops = []
    for trip in rtTrips:
        for row in rows:
            if int(trip.tripId) == int(row[0]):
                thisTrip = trip
            
    if (thisTrip != None):
        theseStops= ParseStops(thisTrip)
    else:
        print("Trip data is unavailable")


    return render_template('route.html', routeName=routeName, stops=theseStops)

if __name__ == "__main__":
    app.run(debug=True)
