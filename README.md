# MTA_App

## stops.txt, trips.txt, routes.txt
These files are provided by the city for developer use. They're comma-delimited and contain the General Transit Feed Specification (GTFS) information for various aspects of the city bus public transportation in Baltimore.

## init_db.py
This script reads in the resource files and insert into 3 tables in the database:
+ stops
+ trips
+ routes

## schema.sql
Ued by `init_db.py` to create the database.

## mta_classes.py
Contains classes to create Vehicle() and Trip() objects from real-time info from the API.

## test.py
Very simple test script to pull real-time vehicle info and real-time trip info from the MTA API and print it.
