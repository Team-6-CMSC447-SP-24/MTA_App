class Trip:
    def __init__(self, tripDict: dict):
        self.id = tripDict.get('id', None)
        tripInfo = tripDict.get('tripUpdate', {})

        tripDetails = tripInfo.get('trip', {})
        self.tripId = tripDetails.get('tripId', None)
        self.startTime = tripDetails.get('startTime', None)
        self.startDate = tripDetails.get('startDate', None)
        self.scheduleRelationship = tripDetails.get('scheduleRelationship', None)
        self.routeId = tripDetails.get('routeId', None)
        self.directionId = tripDetails.get('directionId', None)
        
        self.stopTimeUpdate = tripInfo.get('stopTimeUpdate', None)

        tripVehicle = tripInfo.get('vehicle', None)
        self.vehicleId = tripVehicle.get('id', None) if tripVehicle is not None else None
        
        self.timeStamp = tripInfo.get('timestamp', None)

    def __str__(self):
        if self.vehicleId is not None and self.stopTimeUpdate is not None and not self.vehicleId.startswith("block_"):
            numStops = len(self.stopTimeUpdate)
            s = f"Vehicle {self.vehicleId} has {numStops} stops left." #\n\tTrip {self.tripId}\n\tRoute {self.routeId}"
        else:
            s = ""
        return s


class Vehicle:
    def __init__(self, vehicleDict: dict):
        self.id = vehicleDict['id']
        vehicleInfo = vehicleDict.get('vehicle', {})  # get() to handle missing info if necessary

        trip_info = vehicleInfo.get('trip', {})
        self.tripId = trip_info.get('tripId', None)
        self.startDate = trip_info.get('startDate', None)
        self.routeId = trip_info.get('routeId', None)

        position_info = vehicleInfo.get('position', {})
        self.latitude = position_info.get('latitude', None)
        self.longitude = position_info.get('longitude', None)
        self.bearing = position_info.get('bearing', None)
        self.speed = position_info.get('speed', None)

        self.currentStopSequence = vehicleInfo.get('currentStopSequence', None)
        self.currentStatus = vehicleInfo.get('currentStatus', None)
        self.timestamp = vehicleInfo.get('timestamp', None)
        self.stopId = vehicleInfo.get('stopId', None)

        vehicle_info = vehicleInfo.get('vehicle', {})
        self.vehicleId = vehicle_info.get('id', None)
        self.vehicleLabel = vehicle_info.get('label', None)

        self.occupancyStatus = vehicleInfo.get('occupancyStatus', None)
        self.occupancyPercentage = vehicleInfo.get('occupancyPercentage', None)

    def __str__(self):
        s = f"Vehicle {self.vehicleId} is at {self.latitude}, {self.longitude}."
        return s
