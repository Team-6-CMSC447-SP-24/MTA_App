from api_utils import *
from credentials import google_key
import unittest
from mta_classes import Vehicle, Trip

#1 As a rider, I want to know what route a bus is driving so I get on the right vehicle for my intended destination.

class TestKnowRoute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')
    
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        self.rtVehicles = getRealTimeVehiclePositions()
        self.vehiclesTable = ParseVehicles(self.rtVehicles)
        pass
    
    def tearDown(self):
        pass

    def test_getVehichles(self): #test getRealTimeVehicleUpdates
        self.assertIsNot(len(self.rtVehicles), 0)

    def test_getRoute(self): #test getRouteName
        route = getRouteName(11684)
        self.assertTrue("Downtown" in route)    

    def test_allRoutes(self): #test all routes can be found in parse, test ParseVehicles
        routes = []
        check = 0
        for vehicle in self.rtVehicles:
            routes.append(getRouteName(vehicle.routeId))
        for route in routes:
            check = 0
            for parse in self.vehiclesTable:
                if route in parse['name']:
                    check = 1
            if check == 0:
                break
        self.assertTrue(check, 1)
            
if __name__ == '__main__':
    unittest.main()
