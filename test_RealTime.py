from api_utils import *
from credentials import google_key
import unittest
from mta_classes import Vehicle, Trip

#2 As a commuter, I want to be able to view real-time information for MTA buses so that I can plan my journey more effectively.

class TestReaTime(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')
    
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        self.rtVehicles = getRealTimeVehiclePositions()
        self.rtTrips = getRealTimeTripUpdates()
        self.vehiclesTable = ParseVehicles(self.rtVehicles)
        pass
    
    def tearDown(self):
        pass

    def test_getTrips(self): #test getRealTimeTripUpdates
        self.assertIsNot(len(self.rtTrips), 0)

    def test_getTrip(self): #test getTripName
        trip = getTripName(3475040)
        self.assertTrue("WOODBERRY" in trip)  

    def test_allOccupancy(self): #test if occupancy is not all same (changes)
        occ = []
        check = 0
        for vehicle in self.rtVehicles:
            if vehicle.occupancyStatus not in occ:
                occ.append(vehicle.occupancyStatus)
        for occ_type in occ:
            check = 0
            for parse in self.vehiclesTable:
                if occ is not parse['occupancy']:
                    check = 1
            if check == 0:
                break
        self.assertTrue(check, 1)

if __name__ == '__main__':
    unittest.main()
