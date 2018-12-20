API_KEY = '6c6b183c887046e89d81df9552de02b1'

import sqlite3

import requests

conn = sqlite3.connect('./mtd.db')


def get_routes_by_stop(stop_id, offline=True):
    if offline:
        routes = []
        for result in conn.execute('''select DISTINCT (routes.route_short_name || " " || routes.route_id) from
        routes JOIN trips JOIN stop_times ON 
                                    (routes.route_id = trips.route_id)
                                    AND
                                    (trips.trip_id = stop_times.trip_id)
                                    AND
                                    (stop_times.stop_id = ?) ORDER BY routes.route_id;''', [stop_id]):
            routes.append(result[0])
        return routes
    url = 'https://developer.cumtd.com/api/v2.2/json/getroutesbystop?key=' + API_KEY + '&stop_id=' + str(stop_id)
    response = requests.get(url)
    text = response.json()
    routes = []
    for route_dict in text['routes']:
        routes.append(route_dict['route_short_name'] + ' ' + route_dict['route_id'])
    return routes


def get_stop(stop_id, offline=True):
    if offline:
        stop_dict = {}
        stop_names = []
        lat_long = []
        for stop in conn.execute('''select stop_name, stop_lat, stop_lon from stops where stop_id like ?;''',
                                 (stop_id.split(':')[0] + '%',)):
            stop_names.append(stop[0])
            lat_long.append((stop[1], stop[2]))
        stop_dict = {'stop_names': stop_names, 'lat_long': lat_long}
        return stop_dict
    url = 'https://developer.cumtd.com/api/v2.2/json/getstop?key=' + API_KEY + '&stop_id=' + str(stop_id)
    response = requests.get(url)
    d = response.json()
    stop_dict = {}
    value = []
    lat_long = []
    for stop in d['stops'][0]['stop_points']:
        value.append(stop['stop_name'])
        lat_long.append((stop['stop_lat'], stop['stop_lon']))
    stop_dict['stop_names'] = value
    stop_dict['lat_lons'] = lat_long
    return stop_dict


def get_trip(trip_id, offline=True):
    if offline:
        trips = []
        for trip in conn.execute('''select route_id, trip_headsign from trips where trip_id like ?;''',
                                 (trip_id,)):
            trips.append(trip)
        return trips
    url = 'https://developer.cumtd.com/api/v2.2/json/gettrip?key=' + API_KEY + '&trip_id=' + str(trip_id)
    response = requests.get(url)
    text = response.json()
    trips = []
    for trip_dict in text['trips']:
        trips.append((trip_dict['route_id'], trip_dict['trip_headsign']))
    return trips


def get_stop_times_by_trip(trip_id, offline=True):
    if offline:
        stop_list = []
        for stop in conn.execute('''select arrival_time, departure_time, stop_name from trips JOIN stop_times 
        JOIN stops 
        on 
        (trips.trip_id = stop_times.trip_id)
        and
        (stops.stop_id = stop_times.stop_id)
        and 
        ((trips.trip_id = ?));''', (trip_id,)):
            stop_list.append(stop)
        return stop_list
    url = 'https://developer.cumtd.com/api/v2.2/json/getstoptimesbytrip?key=' + API_KEY + '&trip_id=' + str(trip_id)
    response = requests.get(url)
    text = response.json()
    stop_list = []
    for stop in text['stop_times']:
        stop_list.append((stop['arrival_time'], stop['departure_time'], stop['stop_point']['stop_name']))
    return stop_list


def get_trip_departures_by_route(route_id, offline=True):
    if offline:
        trip_names = []
        for trip in conn.execute('''select trips.route_id, trips.trip_headsign, trips.trip_id, stop_times.departure_time, stops.stop_name
        from trips
        JOIN
        Stop_times
        JOIN
        Stops
        ON trips.trip_id = stop_times.trip_id and
        stop_times.stop_id = stops.stop_id 
        and 
        stop_times.stop_sequence = 0 
        and
        trips.route_id like ?;''', (route_id,)):
            trip_names.append(trip)
        return trip_names


def get_trips_by_route(route_id, offline=True):
    if offline:
        routes = []
        for route in conn.execute(
                '''select route_id, direction_id, trip_headsign from trips where lower(route_id)= ?;''',
                (route_id.lower(),)):
            routes.append(route)
        return routes
    url = 'https://developer.cumtd.com/api/v2.2/json/gettripsbyroute?key=' + API_KEY + '&route_id=' + str(route_id)
    response = requests.get(url)
    text = response.json()
    routes = []
    for time in text['trips']:
        routes.append(time['shape_id'] + ' ' + time['route_id'] + ' ' + time['direction'] + ' ' + time['trip_headsign'])
    return routes



def get_stoptimes_by_stop(stop_id, route_id=None, date=None, offline=True):
    if offline:
        query = '''select trips.route_id, stop_times.arrival_time from stop_times
        JOIN
        trips
        on
        stop_times.trip_id = trips.trip_id and stop_id =? '''
        tokens = [stop_id]
        if route_id is not None:
            query += '''and trips.route_id = ? '''
            tokens = [stop_id, route_id]
        #         conn.execute(query, tokens)
        route_dict = {}
        for stop in conn.execute(query, tokens):
            time = stop[1]
            route = stop[0]
            if route not in route_dict:
                route_dict[route] = [time]
            else:
                route_dict[route].append(time)
        return route_dict
    base_url = 'https://developer.cumtd.com/api/v2.2/json/getstoptimesbystop?key=' + API_KEY + '&stop_id=' + str(
        stop_id)
    if route_id is not None:
        base_url += '&route_id=' + str(route_id)
    if date is not None:
        base_url += '&date=' + str(date)
    response = requests.get(base_url)
    text = response.json()
    route_dict = {}
    for stop in text['stop_times']:
        time = stop['arrival_time']
        route = stop['trip']['route_id']
        if route not in route_dict:
            route_dict[route] = [time]
        else:
            route_dict[route].append(time)
    return route_dict
