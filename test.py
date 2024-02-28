import json
import http.client
import sqlite3
from mta_classes import Vehicle, Trip

swiftlyConnection = http.client.HTTPSConnection("api.goswift.ly")

swiftlyHeaders = {
    'Content-Type': "application/json",
    'Authorization': "1ee674f78037045f5e600a63047d869b"
    }

def getRealTimeVehiclePositions():
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-vehicle-positions?format=json", headers=swiftlyHeaders)
    res = swiftlyConnection.getresponse()
    vehicle_data = json.loads(res.read()) # TODO: Refactor to create Vehicle() objects here and return as list
    return vehicle_data['entity'] # Only return actual vehicle info

def getRealTimeTripUpdates():
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-trip-updates?format=json", headers=swiftlyHeaders)
    swiftlyRes = swiftlyConnection.getresponse()
    trip_data = json.loads(swiftlyRes.read()) # TODO: Refactor to create Trip() objects here and return as list
    return trip_data['entity']

def getRouteName(databaseFile, route_id):
    conn = sqlite3.connect(databaseFile)
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


if __name__ == "__main__":
    database = 'database.db'
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    rtVehicles = getRealTimeVehiclePositions()
    rtTrips = getRealTimeTripUpdates()
    
    for i in rtVehicles:
        if 'trip' in i['vehicle']: # Vehicle only has 'trip' if in service
            currVehicle = Vehicle(i)
            thisRouteName = getRouteName(database, currVehicle.routeId)
            print(f"Vehicle {currVehicle.id} at ({currVehicle.latitude}, {currVehicle.longitude}), driving {thisRouteName}")
                
    for i in rtTrips:
        currTrip = Trip(i)
        if str(currTrip): # Trip returns null str if failed to initialize
            # print(currTrip)
            pass
