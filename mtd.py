API_KEY = "6c6b183c887046e89d81df9552de02b1"
# API key for MTD access, hard coding for now in the file for reproducibility

import sqlite3

import requests

conn = sqlite3.connect("./mtd.db")
# make sure mtd.db is in the working directory. This is an sqlite database


def get_route_id(route_short_name):
    """
    A purely offline method to return the route id given a short name of the route.
    :param route_short_name:
    :return: string route id
    """
    route_id = []
    for route in conn.execute(
        """select route_id from routes where route_short_name like ?;""",
        (route_short_name.split()[0] + "%",),
    ):
        route_id.append(route)
    return route_id


def get_routes_by_stop(stop_id, offline=True):
    """
     Return all routes at a given stop
    :param stop_id: A string representing the unique stop identifier
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of tuples of bus routes such as [(10, West), (1, North)] corresponding to the stops
    """
    if offline:
        routes = []
        for result in conn.execute(
            "select DISTINCT routes.route_short_name, routes.route_id "
            "from routes "
            "JOIN trips "
            "JOIN stop_times "
            "ON (routes.route_id = trips.route_id) "
            "AND (trips.trip_id = stop_times.trip_id) "
            "AND (stop_times.stop_id = ?) "
            "ORDER BY routes.route_id;",
            [stop_id],
        ):
            routes.append((result[0], result[1]))
        return routes
    url = (
        "https://developer.cumtd.com/api/v2.2/json/getroutesbystop?key="
        + API_KEY
        + "&stop_id="
        + str(stop_id)
    )
    response = requests.get(url)
    text = response.json()
    routes = []
    for route_dict in text["routes"]:
        routes.append((int(route_dict["route_short_name"]), route_dict["route_id"]))
    return routes


def get_stop(stop_id, offline=True):
    """
    Return all details at a given stop
    :param stop_id: A string representing the unique stop identifier
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of bus stop names such as ['Illini Union (Island Shelter)',
  'Illini Union (North Side Shelter)',
  'Illini Union (South Side Shelter)'] along with their latitudes and longitudes
    """
    if offline:
        stop_dict = {}
        stop_names = []
        lat_long = []
        for stop in conn.execute(
            """select stop_name, stop_lat, stop_lon from stops where stop_id like ?;""",
            (stop_id.split(":")[0] + "%",),
        ):
            stop_names.append(stop[0])
            lat_long.append((stop[1], stop[2]))
        stop_dict = {"stop_names": stop_names, "lat_long": lat_long}
        return stop_dict
    url = (
        "https://developer.cumtd.com/api/v2.2/json/getstop?key="
        + API_KEY
        + "&stop_id="
        + str(stop_id)
    )
    response = requests.get(url)
    d = response.json()
    stop_dict = {}
    value = []
    lat_long = []
    for stop in d["stops"][0]["stop_points"]:
        value.append(stop["stop_name"])
        lat_long.append((stop["stop_lat"], stop["stop_lon"]))
    stop_dict["stop_names"] = value
    stop_dict["lat_lons"] = lat_long
    return stop_dict


def get_stop_id(stop_name, offline=True):
    """
    Return the potential stop id corresponding to a natural language stop name.
    :param stop_name: An intersection such as Fifth and Daniel or a landmark stop name such as Illini Union
    :param offline: If True, use the database to filter stops that contain the non-stop words of the query; else use the api to return matches with more than 0.8 score
    :return: a list of matching stops and there ids
    """
    if offline:
        stop_id = []
        query = """SELECT stop_id, stop_name FROM stops WHERE """
        tokens = []
        for token in stop_name.split():
            if token.lower() in ["and", "in", "at"]:
                continue
            query += """INSTR(LOWER(stop_name), ?) AND """
            tokens.append(token.lower())
        for stop in conn.execute(query.rstrip(" AND"), tokens):
            stop_id.append(stop)
        return stop_id
    url = (
        "https://developer.cumtd.com/api/v2.2/json/getstopsbysearch?key="
        + API_KEY
        + "&query="
        + str(stop_name)
    )
    response = requests.get(url)
    text = response.json()
    stop_list = []
    for stop in text["stops"]:
        if stop["percent_match"] > 0.8:
            for point in stop["stop_points"]:
                stop_list.append((point["stop_id"], point["stop_name"]))
    return stop_list


def get_stop_times_by_stop(stop_id, route_id=None, date=None, offline=True):
    """
    Returns arrival times of buses for all routes serving a given stop
    :param stop_id: A string representing a unique stop identifier
    :param route_id: An optional string representing a unique route identifier
    :param date: Optional string representing a calender date
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of all arrival times such as 'BROWN ALT': ['07:28:35', '08:28:35', '07:28:35'], 'GREY ALT': ['07:13:00'] corresponding to the stop.
    """
    if offline:

        query = """select trips.route_id, stop_times.arrival_time, trips.trip_id from stop_times
        JOIN
        trips
        on
        stop_times.trip_id = trips.trip_id and stop_id = ? """
        tokens = [stop_id]
        if route_id is not None:
            query += """and trips.route_id = ? """
            tokens = [stop_id, route_id]
        #         conn.execute(query, tokens)
        route_dict = {}
        for stop in conn.execute(query, tokens):
            time = stop[1]
            route = stop[0]
            trip = stop[2]
            if route not in route_dict:
                route_dict[route] = {time: trip}
            else:
                route_dict[route][time] = trip
        return route_dict

    base_url = (
        "https://developer.cumtd.com/api/v2.2/json/getstoptimesbystop?key="
        + API_KEY
        + "&stop_id="
        + str(stop_id)
    )
    if route_id is not None:
        base_url += "&route_id=" + str(route_id)
    if date is not None:
        base_url += "&date=" + str(date)
    response = requests.get(base_url)
    text = response.json()
    route_dict = {}
    for stop in text["stop_times"]:
        time_dict = {stop["arrival_time"]: stop["trip"]["trip_id"]}
        route = stop["trip"]["route_id"]
        if route not in route_dict:
            route_dict[route] = time_dict
        else:
            route_dict[route][stop["arrival_time"]] = stop["trip"]["trip_id"]
    return route_dict


def get_stop_times_by_trip(trip_id, offline=True):
    """
    Return all details of arrival and departure times at all stops for a given trip
    :param trip_id: A string representing the unique trip identifier
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of arrival and departure times such as [('11:14:00', '11:14:00', 'Main & Brady (SW Far Side)'),
 ('11:14:42', '11:14:42', 'Brady & High (NW Corner)'),
 ('11:15:22', '11:15:22', 'MacArthur & California (NW Corner)'),
 ('11:16:02', '11:16:02', 'Washington & MacArthur (NW Corner)'),
 ('11:16:51', '11:16:51', 'Washington & Scottswood (NE Far Side)'),
 ('11:17:31', '11:17:31', 'Scottswood & Illinois (SE Corner)'),
 ('11:18:06', '11:18:06', 'Dodson & Illinois (NE Corner)'),
 ('11:18:56', '11:18:56', 'Dodson & Washington (NW Corner)'),
 ('11:19:17', '11:19:17', 'Washington & Timothy Tr. (North Side)')] corresponding to the trips
    """
    if offline:
        stop_list = []
        for stop in conn.execute(
            """select arrival_time, departure_time, stop_name from trips JOIN stop_times 
        JOIN stops 
        on 
        (trips.trip_id = stop_times.trip_id)
        and
        (stops.stop_id = stop_times.stop_id)
        and 
        ((trips.trip_id = ?));""",
            (trip_id,),
        ):
            stop_list.append(stop)
        return stop_list
    url = (
        "https://developer.cumtd.com/api/v2.2/json/getstoptimesbytrip?key="
        + API_KEY
        + "&trip_id="
        + str(trip_id)
    )
    response = requests.get(url)
    text = response.json()
    stop_list = []
    for stop in text["stop_times"]:
        stop_list.append(
            (
                stop["arrival_time"],
                stop["departure_time"],
                stop["stop_point"]["stop_name"],
            )
        )
    return stop_list


def get_trip(trip_id, offline=True):
    """
    Return all trip details for a given trip
    :param trip_id: A string representing the unique trip identifier
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of trip headsigns such as ['Champaign Meijer', 'Round Barn Road - Holiday Park'] corresponding to the trips
    """
    if offline:
        trips = []
        for trip in conn.execute(
            """select route_id, trip_headsign from trips where trip_id like ?;""",
            (trip_id,),
        ):
            trips.append(trip)
        return trips
    url = (
        "https://developer.cumtd.com/api/v2.2/json/gettrip?key="
        + API_KEY
        + "&trip_id="
        + str(trip_id)
    )
    response = requests.get(url)
    text = response.json()
    trips = []
    for trip_dict in text["trips"]:
        trips.append((trip_dict["route_id"], trip_dict["trip_headsign"]))
    return trips


def get_trip_arrivals_by_stop(trip_id, stop_id):
    """
    Return departure times of all trips for a given route at originating stop
    :param trip_id: A string representing a unique route identifier
    :return: A tuple of arrival times at the given stop of the trip. If the trip does not visit the stop, it returns an empty .
    """
    query = """select DISTINCT trips.trip_id, stop_times.departure_time
    from trips
    JOIN
    Stop_times
    JOIN
    Stops
    ON trips.trip_id = stop_times.trip_id and
    stop_times.stop_id = ?
    and 
    trips.trip_id like ?;"""
    tokens = (stop_id, trip_id)
    trip_names = []
    for trip in conn.execute(query, tokens):
        trip_names.append(trip)
    return trip_names


def get_trips_by_route(route_id, offline=True):
    """
    Return all trips for a given route including trip id
    :param route_id: A string representing a unique route identifier
    :param offline: Optional boolean parameter that determines wether to use the API or the offline database for retrieving results
    :return: A list of routes with it's corresponding headsign such as [( 'GREEN', 'Illini Union'),
 ('GREEN',  'Round Barn Road - Holiday Park')]
    """
    if offline:
        routes = []
        for route in conn.execute(
            """select route_id, direction_id, trip_headsign from trips where lower(route_id)= ?;""",
            (route_id.lower(),),
        ):
            routes.append(route)
        return routes

    url = (
        "https://developer.cumtd.com/api/v2.2/json/gettripsbyroute?key="
        + API_KEY
        + "&route_id="
        + str(route_id)
    )
    response = requests.get(url)
    text = response.json()
    routes = []
    for time in text["trips"]:
        routes.append((time["route_id"], time["direction"], time["trip_headsign"]))
    return routes
