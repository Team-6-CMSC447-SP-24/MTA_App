-- Several values in each table are unused; they're included for the sake of completion

DROP TABLE IF EXISTS stops;
CREATE TABLE stops (
    stop_id INTEGER PRIMARY KEY NOT NULL,
    stop_code INTEGER,
    stop_name TEXT NOT NULL,
    stop_desc TEXT,
    stop_lat FLOAT,
    stop_lon FLOAT,
    zone_id INTEGER,
    stop_url TEXT,
    location_type INTEGER,
    parent_station INTEGER,
    stop_timezone TEXT,
    wheelchair_boarding INTEGER,
    direction TEXT,
    position TEXT
);

DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
    route_id INTEGER,
    service_id INTEGER,
    trip_id INTEGER PRIMARY KEY NOT NULL,
    trip_headsign TEXT NOT NULL,
    trip_short_name INTEGER,
    direction_id INTEGER,
    block_id INTEGER,
    shape_id INTEGER,
    wheelchair_accessible INTEGER,
    bikes_allowed INTEGER
);

DROP TABLE IF EXISTS routes;
CREATE TABLE routes (
    route_id INTEGER NOT NULL,
    agency_id INTEGER,
    route_short_name TEXT NOT NULL,
    route_long_name TEXT NOT NULL,
    route_desc TEXT,
    route_type INTEGER,
    route_url TEXT,

    -- route_color and route_text_color both given as hex ints
    route_color TEXT,
    route_text_color TEXT,
    
    network_id TEXT,
    as_route INTEGER
);

DROP TABLE IF EXISTS logins;
CREATE TABLE logins (
    username TEXT PRIMARY KEY NOT NULL,
    hashed_password TEXT NOT NULL
);

DROP TABLE IF EXISTS favorites;
CREATE TABLE favorites (
    username TEXT NOT NULL,
    route_name TEXT NOT NULL,
    route_id TEXT NOT NULL
);