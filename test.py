import json
import http.client
import sqlite3
from mta_classes import Vehicle, Trip

database = 'database.db'
swiftlyConnection = http.client.HTTPSConnection("api.goswift.ly")

swiftlyHeaders = {
    'Content-Type': "application/json",
    'Authorization': "1ee674f78037045f5e600a63047d869b"
    }

def getRealTimeVehiclePositions():
    allVehicles = []
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-vehicle-positions?format=json", headers=swiftlyHeaders)
    res = swiftlyConnection.getresponse()
    vehicle_data = json.loads(res.read())
    for i in vehicle_data['entity']:
        if 'trip' in i['vehicle']: # Vehicle only has 'trip' if in service
            currVehicle = Vehicle(i)
            allVehicles.append(currVehicle)
    return  allVehicles

def getRealTimeTripUpdates():
    allTrips = []
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-trip-updates?format=json", headers=swiftlyHeaders)
    swiftlyRes = swiftlyConnection.getresponse()
    trip_data = json.loads(swiftlyRes.read()) # TODO: Refactor to create Trip() objects here and return as list
    for i in trip_data['entity']:
        currTrip = Trip(i)
        if str(currTrip):
            allTrips.append(currTrip)
    return allTrips

def getRouteName(database, route_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    try:
        query = "SELECT route_long_name FROM routes WHERE route_id = ?"
        cursor.execute(query, (route_id,))
        row = cursor.fetchone()
        
        if row:
            thisRouteName = row[0]
            return thisRouteName
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error reading from the database: {e}")
    finally:
        conn.close()
    return

def getStopName(database, stop_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    try:
        query = "SELECT stop_name FROM stops WHERE stop_id = ?"
        cursor.execute(query, (stop_id,))
        row = cursor.fetchone()
        
        if row:
            thisStopName = row[0]
            return thisStopName
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error reading from the database: {e}")
    finally:
        conn.close()
    return

def getTripName(database, trip_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    try:
        query = "SELECT trip_headsign FROM trips WHERE trip_id = ?"
        cursor.execute(query, (trip_id,))
        row = cursor.fetchone()
        if row:
            thistripName = row[0]
            return thistripName
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error reading from the database: {e}")
    finally:
        conn.close()
    return

def showAllTrips(tripsList):
    for trip in tripsList:
        thisName = getRouteName(database, trip.routeId)
        print(f'\n{thisName}')
        count = 1
        for i in range (len(trip.stopTimeUpdate)):
            print(f'{count}.\t{getStopName(database, trip.stopTimeUpdate[i]['stopId'])}')
            count +=1
    return

def showAllVehicles(vehiclesList):
    for vehicle in vehiclesList:
        thisRouteName = getRouteName(database, vehicle.routeId)
        print(f"Vehicle {vehicle.id} at ({vehicle.latitude}, {vehicle.longitude}), driving {thisRouteName}")
    return

if __name__ == "__main__":    
    rtVehicles = getRealTimeVehiclePositions()
    rtTrips = getRealTimeTripUpdates()
    
    showAllVehicles(rtVehicles)
    showAllTrips(rtTrips)
    