import sqlite3
import csv
import requests
import zipfile
import io
import os
from datetime import datetime
import bcrypt
database = 'database.db'

def initRoutesTable(cur: sqlite3.Cursor) -> None:
    
    routes = []
    with open("resources/routes.txt", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            routes.append(dict(row))
    
    for entry in routes:
        sql = """
            INSERT INTO routes 
            (route_id, agency_id, route_short_name, route_long_name, route_desc, 
            route_type, route_url, route_color, route_text_color, network_id, as_route) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            int(entry["route_id"]),
            int(entry["agency_id"]),
            entry["route_short_name"],
            entry["route_long_name"],
            entry["route_desc"],
            int(entry["route_type"]),
            entry["route_url"],
            entry["route_color"],
            entry["route_text_color"],
            entry["network_id"],
            int(entry["as_route"])
        )
        cur.execute(sql, params)
    return

def initTripsTable(cur: sqlite3.Cursor) -> None:

    trips = []
    with open("resources/trips.txt", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            trips.append(dict(row))
    for entry in trips:
        sql = """
            INSERT INTO trips 
            (route_id, service_id, trip_id, trip_headsign, trip_short_name, 
            direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            int(entry["route_id"]),
            int(entry["service_id"]),
            int(entry["trip_id"]),
            entry["trip_headsign"],
            entry["trip_short_name"],
            int(entry["direction_id"]),
            int(entry["block_id"]),
            int(entry["shape_id"]),
            int(entry["wheelchair_accessible"]),
            int(entry["bikes_allowed"]),
        )
        cur.execute(sql, params)
    return

def initStopsTable(cur: sqlite3.Cursor) -> None:
    
    stops = []
    with open("resources/stops.txt", "r") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            stops.append(dict(row))
    for entry in stops:
        sql = """
            INSERT INTO stops 
            (stop_id, stop_code, stop_name, stop_desc, stop_lat, stop_lon, 
            zone_id, stop_url, location_type, parent_station, stop_timezone, 
            wheelchair_boarding, direction, position) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            int(entry["stop_id"]),
            int(entry["stop_code"]),
            entry["stop_name"],
            entry["stop_desc"],
            float(entry["stop_lat"]),
            float(entry["stop_lon"]),
            entry["zone_id"],
            entry["stop_url"],
            entry["location_type"],
            entry["parent_station"],
            entry["stop_timezone"],
            int(entry["wheelchair_boarding"]),
            entry["direction"],
            entry["position"]            
        )
        cur.execute(sql, params)

    return

def updateResourceFiles():
    url = "https://feeds.mta.maryland.gov/gtfs/local-bus"
    files_to_extract = ["stops.txt", "trips.txt", "routes.txt"]
    output_directory = "./resources"
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to download the ZIP file from {url}")
        return


    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        for file_name in files_to_extract:
            if file_name in zip_file.namelist():
                zip_info = zip_file.getinfo(file_name)
                output_file_path = os.path.join(output_directory, file_name)
                overwrite_file = True

                if os.path.exists(output_file_path):
                    existing_file_mtime = datetime.fromtimestamp(os.path.getmtime(output_file_path))
                    zip_file_mtime = datetime.fromtimestamp(zip_info.date_time[5])

                    if zip_file_mtime <= existing_file_mtime:
                        overwrite_file = False

                if overwrite_file:
                    zip_file.extract(file_name, output_directory)
                    print(f"Extracted {file_name} to {output_directory}")
                else:
                    print(f"Skipping {file_name} as it's not newer than the existing file")
            else:
                print(f"{file_name} not found in the ZIP file")

def initLoginsTable(cur: sqlite3.Cursor) -> None:

    logins = [{"username":"admin", "password": "admin"}, 
              {"username":"test", "password": "test"}, 
              {"username":"randall", "password": "CorrectHorseBatteryStaple"}
              ]
    
    for entry in logins:
        sql = """
            INSERT INTO logins
            (username, hashed_password) 
            VALUES (?, ?)
        """
        salt = bcrypt.gensalt()
        params = (
            entry["username"],
            bcrypt.hashpw(entry["password"].encode("utf-8"), salt)
        )
        cur.execute(sql, params)
    return
    

if __name__ == "__main__":
    updateResourceFiles()

    connection = sqlite3.connect(database)
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()

    initRoutesTable(cur)
    initTripsTable(cur)
    initStopsTable(cur)
    initLoginsTable(cur)

    connection.commit()
    connection.close()
    
    print("Successful init")