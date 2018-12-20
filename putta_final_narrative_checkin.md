Final Project
=============

Regular commuters using the Champaign Urbana Mass Transit District (MTD) buses rely on web and mobile apps to track bus arrivals at bus stops. These apps run based on the developer application programming interface (API) provided by MTD (developer.cumtd.com/). This programming project aims to produce a python-based wrapper for the API. The goal is to create functions in python that leverage the API and parse the jsonl results into native python data structures such as lists and dictionaries. Additionally, the fixed list of bus stops and scheduled times are populated in a sqlite database for offline access. Some of the functions fall back on the sqlite database if there is no internet access.

Github URL: https://github.com/sarvaniputta/is452_final_project

**Narrative**:
------------

We registered at http://developer.cumtd.com/ and obtained an API Key from MTD website and used it as a key for the future API access. We also downloaded a dump of the transit feed data in the form of csv files from https://developer.cumtd.com/gtfs/google_transit.zip. The feed includes all the stops, routes, trips, schedule info, and geographic data for the transit system and the format is documented at https://developers.google.com/transit/gtfs/reference/?csw=1. We leverage this data by importing it into corresponding tables in a sqlite database `mtd.db`. Since, the schedule info does not change regularly, it is possible to obtain useful information completely offline from the sqlite database. To do this, we structure our functions as follows
```
def api_method(args, offline=True):
    if offline:
        # return results from sql query
    # return results from json result of calling REST api
```
This template has the advantage of using the `offline` argument to create one function that can return results from offline or online sources. 

We imported requests library http://docs.python-requests.org/en/master/ to access the REST API of MTD. When using the online methods, each api method corresponds to an URL that is constructed with the passed arguments. Using the requests.get method, we ping the URL and obtain the json response. The json response can be parsed and combined with the accumulator pattern to create an appropriate data structure to return. To use the `offline` argument, a connection to the database is created in the library using the `sqlite3` library. When the `offline` argument is `True`, the function executes a parametrized query which is mostly fixed on the database using the connection object. The parameters are substituted from the arguments to the function. 


Below is a list of the functions we define in `mtd.py` file.

`get_route_id` is a purely offline method to obtain the route_id from a route number or short name. There is no equivalent in the API.

`get_routes_by_stop` is a method which emulates the GetRoutesByStop API method. Here, we are interested in getting the details of a route. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. We send a get requests to the URL and parse the JSON response. The response is a dictionary and we used the item corresponding to the routes key which is a list containing route_color, route_id, route_long_name, route_short_name, route_text_color. We used an accumulator variable called routes to collect the details. We then return the list of details. If the offline parameter is True, then we join the routes, stops and trips tables to extract the same details.


`get_stop` is a method which emulates the GetStop API method. Here, we are interested in getting the details of a stop. The original method takes a mandatory parameter called stop_id. Similarly, we pass a stop_id as an argument and use it to create the appropriate URL. The response from the URL is a dictionary and we used the item corresponding to the stops key. Each stop can contain multiple stop points, presented as a list corresponding to stop points key. We iterate through the stop_points value to collect the latitude, longitude and the name of each stop point. We used two accumulator variables to collect the details and create a dictionary of the results. The offline version is easier as the stops table contains all the details and returns the results as a tuple. Using two accumulator variables, we can create the result dictionary

`get_stop_id` is a method that takes an intersection or stop name in natural language and returns all matching stop_ids. When offline, it uses a simple non stop-word matching in the database. So 'Fifth and Daniel' as input would return all stops which have both Fifth and Daniel in their name. The online version uses the API which provides the matches and a similarity score 0-1 directly. Using the accumulator pattern we only list those matches which have a similarity score greater than 0.8

`get_stop_times_by_stop` is a method which emulates the GetStopTimesByStop API method . The original method takes stop_id as a mandatory argument while taking date and route_id as optional parameters. So we used them similarly in our method by giving the default values for route_id and date as None and created a URL from the arguments. Depending on the number of the passes arguments, we modify the URL appropriately. We then send a get request to the URL and parse the JSON response. The response is a dictionary and we used the value corresponding to the stop_times key. We used a dictionary accumulator to collect the arrival times of all the routes serving a given stop, with routes being the key and a list of arrival times of each route as the corresponding value.

`get_stop_times_by_trip` is a method which emulates the GetStopTimesByTrip API method. To get the details of a particular trip, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the stop_times key in the response dictionary. We used an accumulator variable called stop_list to collect the details. We then return the list of details.

`get_trip` is a method which emulates the GetTrip API method. To get the details of a particular trip, we pass a trip_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the trips key in the response dictionary, which is a list containing the details of the trip. We further used an accumulator variable called trips to collect the details. We then return the list of details.

`get_trip_arrivals_by_stop` is a method to obtain the arrival time of a particular trip at a given stop. It does not have a corresponding API method and was designed for user convenience. The lack of an API method means, we need to utilize the offline database to join trips, stops and stop_times tables appropriately and return the time a particular trip stops at a given stop id. If a trip does not stop, the sql query returns no results, which implies the method itself returns an empty list.

`get_trips_by_route` is a method which emulates the GetTripsByRoute API method. To get the details of a particular trip, we pass a route_id as an argument and use it to create the appropriate URL. We send a get request to the URL and parse the JSON response. We used the value corresponding to the trips key in the response dictionary, which is a list containing the details of the trip. We used an accumulator variable called routes to collect the details. We then return the list of details.


Lessons Learnt
==============

This project was chosen as a portfolio project demonstrating skills learnt in IS452. The functions utilize the accumulator pattern heavily by creating lists, tuples and dictionaries out of the database results and json parsing. The project also heavily involved concepts such as parsing dictionaries formed from json, writing SQL queries and structuring databases and optional and mandatory arguments in python. Apart from SQL, I was first introduced to the other concepts during the lectures. Aside from this, completing the project also involved learning git and github and libraries such as `requests` and `sqlite3`.  I learnt a lot about git from tutorial at Atlassian and Github, while StackExchange helped with requests library. The API itself was well documented and was easy to use, making the learning curve a little less steep. Also, I use the bus daily and was able to make sense of the data from the API from my experience. Overall, this is my first individual project with python and I plan to showcase this on my github in my resume. 
