from flask import Flask, render_template, request, url_for, flash, redirect, abort
from api_utils import *
from credentials import google_key
import unittest

#1 As a rider, I want to know what route a bus is driving so I get on the right vehicle for my intended destination.
#2 As a commuter, I want to be able to view real-time information for MTA buses so that I can plan my journey more effectively.
#3 As a user, I want to be able to view the full schedule for a specific route so that I can plan my journey in advance.
#4 As a user, I want to be able to search for specific bus or train routes so that I can quickly find the information I need.

class TestKnowRoute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')
    
    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_X(self):
        pass