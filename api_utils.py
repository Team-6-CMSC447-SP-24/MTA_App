import json
import http.client
import sqlite3
from mta_classes import Vehicle, Trip
from flask import Flask, render_template, request
from credentials import mta_key, google_key
import bcrypt

database = 'database.db'
swiftlyConnection = http.client.HTTPSConnection("api.goswift.ly")

swiftlyHeaders = {
    'Content-Type': "application/json",
    'Authorization': mta_key
    }

def getRealTimeVehiclePositions() -> list[Vehicle]:
    allVehicles = []
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-vehicle-positions?format=json", headers=swiftlyHeaders)
    res = swiftlyConnection.getresponse()
    vehicle_data = json.loads(res.read())
    for i in vehicle_data['entity']:
        if 'trip' in i['vehicle']: # Vehicle only has 'trip' if in service
            currVehicle = Vehicle(i)
            allVehicles.append(currVehicle)
    return  allVehicles

def getRealTimeTripUpdates() -> list[Trip]:
    allTrips = []
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-trip-updates?format=json", headers=swiftlyHeaders)
    swiftlyRes = swiftlyConnection.getresponse()
    trip_data = json.loads(swiftlyRes.read()) # TODO: Refactor to create Trip() objects here and return as list
    for i in trip_data['entity']:
        currTrip = Trip(i)
        if str(currTrip):
            allTrips.append(currTrip)
    return allTrips

def getRouteName(route_id: str) -> str:
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
        conn.commit()
        conn.close()
    return

def getStopName(stop_id: str) -> str:
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

def getStopCoords(stop_id: int) -> tuple[str, str]:
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    try:
        query = "SELECT stop_lat, stop_lon FROM stops WHERE stop_id = ?"
        cursor.execute(query, (stop_id,))
        row = cursor.fetchone()

        if row:
            thisStopLat, thisStopLon = row
            return (thisStopLat, thisStopLon)
        else:
            return None
    except sqlite3.Error as e:
        print(f"Error reading from the database: {e}")
    finally:
        conn.close()

def getTripName(trip_id: str) -> str:
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

def ParseVehicles(currentVehicles: list[Vehicle]) -> list[dict[str, str]]:
    tableInfo = []
    for vehicle in currentVehicles:
        tableInfo.append({'busId': vehicle.id,
                          'tripId': vehicle.tripId,
                          'name': getRouteName(vehicle.routeId), 
                          'occupancy': ParseOccupancy(vehicle.occupancyStatus),
                          })
    tableInfo_sorted = sorted(tableInfo, key=lambda x: x['name'])
    return tableInfo_sorted

def ParseStops(currentTrip: Trip) -> list[dict[str, str]]:
    seqNum = ""
    name = ""
    theseStops = []
    for i in range (len(currentTrip.stopTimeUpdate)):
        seqNum = currentTrip.stopTimeUpdate[i]['stopSequence']
        name = getStopName(currentTrip.stopTimeUpdate[i]['stopId'])
        theseStops.append({'seq': seqNum, 'name': name})
    return theseStops

def ParseOccupancy(status: str) -> str:
    thisStatus = ""
    if status == 'EMPTY':
        thisStatus = 'Empty'
    elif status == 'MANY_SEATS_AVAILABLE':
        thisStatus = 'Many seats'
    elif status == 'FEW_SEATS_AVAILABLE':
        thisStatus = 'Few seats'
    elif status == 'STANDING_ROOM_ONLY':
        thisStatus = 'Standing'
    elif status == 'CRUSHED_STANDING_ROOM_ONLY':
        thisStatus = 'Crushed'
    elif status == 'FULL':
        thisStatus = 'Full'
    elif status == 'NOT_ACCEPTING_PASSENGERS':
        thisStatus = 'Not accepting'
    else:
        thisStatus = 'Not reported'
    return thisStatus

def showAllTrips(tripsList: list[Trip]) -> None:
    for trip in tripsList:
        thisName = getRouteName(trip.routeId)
        print(f'\n{thisName}')
        count = 1
        for i in range (len(trip.stopTimeUpdate)):
            curr = trip.stopTimeUpdate[i]['stopId']
            name = getStopName(curr)
            lat, lon = getStopCoords(curr)
            print(f"{count}.\t{name} ({lat}, {lon})")
            count +=1
    return

def showAllVehicles(vehiclesList: list[Vehicle]) -> None:
    for vehicle in vehiclesList:
        thisRouteName = getRouteName(vehicle.routeId)
        print(f"Vehicle {vehicle.id} at ({vehicle.latitude}, {vehicle.longitude}), driving {thisRouteName}")
    return

def searchBusId(bus_id, vehicles: list[Vehicle]):
    acceptedVehicles = []
    for vehicle in vehicles:
        if bus_id in vehicle.id:
            acceptedVehicles.append(vehicle)
    return acceptedVehicles

def searchTripId(trip_id, vehicles: list[Vehicle]):
    acceptedVehicles = []
    for vehicle in vehicles:
        if trip_id in vehicle.tripId:
            acceptedVehicles.append(vehicle)
    return acceptedVehicles

def searchRouteName(route_name, vehicles: list[Vehicle]):
    acceptedVehicles = []
    for vehicle in vehicles:
        if route_name in getRouteName(vehicle.route):
            acceptedVehicles.append(vehicle)
    return acceptedVehicles

def findStop(stop_name, currentTrip: Trip) -> int:
    seqNum = ""
    name = ""
    theseStops = []
    for i in range (len(currentTrip.stopTimeUpdate)):
        seqNum = currentTrip.stopTimeUpdate[i]['stopSequence']
        if stop_name in getStopName(currentTrip.stopTimeUpdate[i]['stopId']):
            return 1
    return 0

def searchStopName(stop_name, trips: list[Trip], vehicles : list[Vehicle]): #Can shorten time complexity if its possible to make a Vehicle variable in Trip
    acceptedVehicles = []
    vehicleIds = []
    for trip in trips:
        if findStop(stop_name, trip):
            if trip.vehicleId not in vehicleIds:
                vehicleIds.append(trip.vehicleId)
                for vehicle in vehicles:
                    if vehicle.vehicleId == trip.vehicleId:
                        acceptedVehicles.append(vehicle)
    return acceptedVehicles

def isValidLogin(username: str, password: str) -> bool:
    connection = sqlite3.connect(database)
    cur = connection.cursor()

    cur.execute("SELECT username, hashed_password FROM logins WHERE username = ?", (username,))
    results = cur.fetchall()
    if results:
        storedUsername, storedHash = results[0]
        if bcrypt.checkpw(password.encode("utf-8"), storedHash):
            return True
    return False

def findUser(username: str) -> bool:
    connection = sqlite3.connect(database)
    cur = connection.cursor()

    cur.execute("SELECT username, hashed_password FROM logins WHERE username = ?", (username,))
    results = cur.fetchall()
    connection.commit()
    connection.close()
    return results

def main() -> None:
    rtVehicles = getRealTimeVehiclePositions()
    rtTrips = getRealTimeTripUpdates()
    showAllVehicles(rtVehicles)
    showAllTrips(rtTrips)
    
    thisUser = input("Username: ")
    if not findUser(thisUser):
        print("Invalid user")
    else:
        thisPassword = input("Password: ")
        if isValidLogin(thisUser, thisPassword):
            print(f"Valid login")
        else:
            print(f"Invalid login")

if __name__ == "__main__":
    main()
