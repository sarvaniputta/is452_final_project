We registered at http://developer.cumtd.com/ and obtained an API Key from MTD website and used it as a key for the future API access.


We imported two libraries namely, requests http://docs.python-requests.org/en/master/ and pprint for better formatting and exploration of dictionaries.


get_routes_by_stop() is a method which emulates the API method, GetRoutesByStop. Here, we are interested in getting the details of route. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the routes key which is a list containing route_color, route_id, route_long_name, route_short_name, route_text_color. We used an accumulator variable called routes to collect the details. We then return the list of details.


get_stop() is a method which emulates the API method, GetStop. Here, we are interested in getting the details of stop. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the stops key. Each stop can contain multiple stop points, presented as a list corresponding to stop points key.We iterate through the stop_points value to collect the latitude, longitude and the name of each stop point. We used two accumulator variables to collect the details and create a dictionary of the results.


get_trip() is a method which emulates the API method, GetTrip. Here, we are interested in getting the details of a particular trip. The original method takes a mandatory parameter called trip_id. Similarly, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the trips key which is a list containing id, headsign, route's id, block's id, direction, service id, and the shape id. We used an accumulator variable called trips to collect the details. We then return the list of details.






get_stop_times_by_trip() is a method which emulates the API method, GetStopTimesByTrip. Here, we are interested in getting the details of a particular trip. The original method takes a mandatory parameter called trip_id. Similarly, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the stop_times key which is a list containing the details of the stop. We used an accumulator variable called stop_list to collect the details. We then return the list of details.



get_trips_by_route() is a method which emulates the API method, GetTripsByRoute. Here, we are interested in getting the details of a particular route. The original method takes a mandatory parameter called route_id. Similarly, we pass a route_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the trips key which is a list containing the details of the trip. We used an accumulator variable called routes to collect the details. We then return the list of details.



get_stoptimes_bystop is a method which emulates the API method GetStopTimesByStop. The original method takes stop_id as a mandatory argument while taking date and route_id as optional parameters. So we used them similarly in our method by giving the values for route_id and date to be None and created a URL. Firstly, the value of route id is checked by using a conditional statement. If the value is not None, the URL has to be modified appropriately and similarly for the date. We then send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the stop_times key. We used dictionary accumulator to collect the arrival times of all the routes serving a given stop. 


