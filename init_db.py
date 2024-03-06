import sqlite3
import csv

def initRoutesTable(thisCur: sqlite3.Cursor) -> None:
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
        thisCur.execute(sql, params)

    return

def initTripsTable(thisCur: sqlite3.Cursor) -> None:
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
        thisCur.execute(sql, params)
        
    return

def initStopsTable(thisCur: sqlite3.Cursor) -> None:
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
        thisCur.execute(sql, params)
        
    return

if __name__ == "__main__":
    connection = sqlite3.connect('database.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()

    initRoutesTable(cur)
    initTripsTable(cur)
    initStopsTable(cur)

    print("Successful init")
    
    connection.commit()
    connection.close()
