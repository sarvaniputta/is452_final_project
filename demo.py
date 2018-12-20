from pprint import pprint

import mtd

# This file demonstrates the use of the mtd.py collection of functions.

# Let us imagine, we need are at the Illinois Union and want to find what buses are available to go Urbana Meijer

# Each stop is identified by a stop id. We can get the stop id for the Union as follows.
pprint(mtd.get_stop_id("Illini Union"))
# [('IU:9', 'Illini Union (Island Shelter)'),
#  ('IU:2', 'Illini Union (North Side Shelter)'),
#  ('IU:1', 'Illini Union (South Side Shelter)')]

# We want to get all the routes through IU South Side Shelter
routes_union = mtd.get_routes_by_stop("IU:1", offline=False)
pprint(routes_union)
# [(8, 'BRONZE'),
#  (10, 'GOLD'),
#  (5, 'GREEN'),
#  (50, 'GREEN EVENING') ...]
# Each route is a tuple comprising of the route number (short name) and the string route id


# We will be taking the Red line to Meijer. So we want to get all trips of the route 'RED' with arrival times at the Union
red_line_trips = mtd.get_stop_times_by_stop(stop_id="IU:1", route_id="RED", offline=True)
pprint(red_line_trips)
# {'RED': {'06:43:00': '[@15.0.68512636@][42][1375907660889]/1__R3_MF',
#          '07:01:00': '[@14.0.56288404@][2][1302877258501]/4__R4_MF',
#          '07:48:00': '[@14.0.56288404@][2][1303306853233]/2__R1_MF',
#          '08:16:00': '[@14.0.56288404@][2][1303306853233]/3__R2_MF',
#          '08:54:00': '[@14.0.56288404@][2][1304020391461]/0__R3_MF', .. }


# We will take  07:01 trip to Meijer. First we get the stop_id for Meijer
pprint(mtd.get_stop_id("Urbana Meijer"))
# [('URBMEIJ:2', 'Urbana Meijer (North Side)'),
#  ('URBMEIJ:1', 'Urbana Meijer (South Side)')]
# We use the stop id for Meijer and the trip id for the 07:01 trip at the Union to find when we will arrive at Meijer.
pprint(
    mtd.get_trip_arrivals_by_stop(
        "[@14.0.56288404@][2][1302877258501]/4__R4_MF", "URBMEIJ:1"
    )
)
# [('[@14.0.56288404@][2][1302877258501]/4__R4_MF', '07:14:00')]
# So we will arrive by 07:14 at Urbana Meijer

# I want to get the headsign on the bus for the trip
trip_info = mtd.get_trip("[@14.0.56288404@][2][1302877258501]/4__R4_MF", offline=False)
pprint(trip_info)
# [('RED', 'Lincoln Square')]
# So I need to get on the bus marked Lincoln Square

# Since, this is my first time on this bus, I want to know what stops this trip services. I can get the information as follows.
pprint(mtd.get_stop_times_by_trip("[@14.0.56288404@][2][1302877258501]/4__R4_MF", offline=True))


# From the results we get the stop ids for the various stops at the Union. Say we are interested in the south side shelter (closest to the union)
# We can get latitude, longitude and other details as follows
union_info = mtd.get_stop("IU:1")
pprint(union_info)
