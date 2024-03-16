from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *
from credentials import google_key
import unittest

#3 As a user, I want to be able to view the full schedule for a specific route so that I can plan my journey in advance.

class TestFullSchedule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')
    
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        self.rtVehicles = getRealTimeVehiclePositions()
        self.vehiclesTable = ParseVehicles(self.rtVehicles)
        self.rtTrips = getRealTimeTripUpdates()
        pass
    
    def tearDown(self):
        pass
    
    def test_getStop(self): #test getStopName
        stop = getStopName(1)
        self.assertTrue("Cylburn" in stop)  

    def test_parseStops(self): #test parseStops, test each trip will show ALL stops
        stops = []
        check = 0
        for trip in self.rtTrips:
            stops.append({trip.tripId: ParseStops(trip)})
        for vehicle in self.rtVehicles:
            for stop in stops:
                if vehicle.tripId in stop:
                    check = 1
                    if len(stop[vehicle.tripId]) <= 0:
                        self.assertTrue(check, -1)
            if check == 0:
                break
        self.assertTrue(check, 1)

if __name__ == '__main__':
    unittest.main()
