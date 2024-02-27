import json
import http.client
from mta_classes import Vehicle, Trip

swiftlyConnection = http.client.HTTPSConnection("api.goswift.ly")

headers = {
    'Content-Type': "application/json",
    'Authorization': "1ee674f78037045f5e600a63047d869b"
    }

def rtVehiclePositions():
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-vehicle-positions?format=json", headers=headers)
    res = swiftlyConnection.getresponse()
    vehicle_data = json.loads(res.read())
    return vehicle_data['entity'] # Only return actual vehicle info

def rtTripUpdates():
    swiftlyConnection.request("GET", "/real-time/mta-maryland/gtfs-rt-trip-updates?format=json", headers=headers)
    swiftlyRes = swiftlyConnection.getresponse()
    trip_data = json.loads(swiftlyRes.read())
    return trip_data['entity']

if __name__ == "__main__":
    rtVehicles = rtVehiclePositions()
    for i in rtVehicles:
        if 'trip' in i['vehicle']: # Vehicle only has 'trip' if in service
            print(f'{Vehicle(i)}')
    
    
    rtTrips = rtTripUpdates()
    for i in rtTrips:
        currTrip = Trip(i)
        if str(currTrip): # Trip returns null str if failed to initialize
            print(currTrip)