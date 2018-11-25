from pprint import pprint

import mtd

union_info = mtd.get_stop('IU:1')
pprint(union_info)

routes_union = mtd.get_routes_by_stop('IU:1')
pprint(routes_union)

red_line_trips = mtd.get_trips_by_route('RED')
pprint(red_line_trips)

trip_info = mtd.get_trip('20RED009__R1SA')
pprint(trip_info)

red_line_stops = mtd.get_stop_times_by_trip('20RED009__R1SA')
pprint(red_line_stops)
