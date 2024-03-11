import json
import http.client
import sqlite3
from mta_classes import Vehicle, Trip
from flask import Flask, render_template, request

database = 'database.db'
swiftlyConnection = http.client.HTTPSConnection("api.goswift.ly")

swiftlyHeaders = {
    'Content-Type': "application/json",
    'Authorization': "1ee674f78037045f5e600a63047d869b"
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
            print(f"{count}.\t{getStopName(trip.stopTimeUpdate[i]['stopId'])}")
            count +=1
    return

def showAllVehicles(vehiclesList: list[Vehicle]) -> None:
    for vehicle in vehiclesList:
        thisRouteName = getRouteName(vehicle.routeId)
        print(f"Vehicle {vehicle.id} at ({vehicle.latitude}, {vehicle.longitude}), driving {thisRouteName}")
    return

def main() -> None:
    rtVehicles = getRealTimeVehiclePositions()
    rtTrips = getRealTimeTripUpdates()
    showAllVehicles(rtVehicles)
    showAllTrips(rtTrips)
    

if __name__ == "__main__":
    main()
