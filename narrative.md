We registered at http://developer.cumtd.com/ and obtained an API Key from MTD website and used it as a key for the future API access.


We imported requests library http://docs.python-requests.org/en/master/ to access the REST API of MTD.


get_routes_by_stop() is a method which emulates the GetRoutesByStop API method. Here, we are interested in getting the details of a route. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the routes key which is a list containing route_color, route_id, route_long_name, route_short_name, route_text_color. We used an accumulator variable called routes to collect the details. We then return the list of details.


get_stop() is a method which emulates the GetStop API method. Here, we are interested in getting the details of a stop. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. The response from the URL is a dictionary and we used the item corresponding to the stops key. Each stop can contain multiple stop points, presented as a list corresponding to stop points key. We iterate through the stop_points value to collect the latitude, longitude and the name of each stop point. We used two accumulator variables to collect the details and create a dictionary of the results.


get_trip() is a method which emulates the GetTrip API method. To get the details of a particular trip, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the trips key in the response dictionary, which is a list containing the details of the trip. We further used an accumulator variable called trips to collect the details. We then return the list of details.


get_stop_times_by_trip() is a method which emulates the GetStopTimesByTrip API method. To get the details of a particular trip, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the stop_times key in the response dictionary. We used an accumulator variable called stop_list to collect the details. We then return the list of details.



get_trips_by_route() is a method which emulates the GetTripsByRoute API method. To get the details of a particular trip, we pass a route_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the trips key in the response dictionary, which is a list containing the details of the trip. We used an accumulator variable called routes to collect the details. We then return the list of details.



get_stoptimes_bystop is a method which emulates the GetStopTimesByStop API method . The original method takes stop_id as a mandatory argument while taking date and route_id as optional parameters. So we used them similarly in our method by giving the default values for route_id and date as None and created a URL from the arguments. Depending on the number of the passes arguments, we modify the URL appropriately. We then send a get request to the URL and parse the JSON response. The response is a dictionary and we used the value corresponding to the stop_times key. We used a dictionary accumulator to collect the arrival times of all the routes serving a given stop, with routes being the key and a list of arrival times of each route as the corresponding value.


