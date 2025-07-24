from AppData import MAP_TILE_RESOLUTION
from requests import get


class NavigationAPI:
    """
    a class to communicate with various mapping services:
        -> GraphHopper connection for routing       port: 8989
        -> TileServer-GL connection for map tiles   port: 8080
        -> Nominatim connection for geocoding       port: 8088
        -> BN-220 GPS module for location           port: /dev/ttyAMA0
    """

    GPS_COORDS = (37.21958541870117, -80.39937591552734)  # todo hook up to gps module for live location
    NOMINATIM_URL = "http://localhost:8088/search"
    GRAPH_HOPPER_URL = "http://localhost:8989/route"

    def __init__(self, map_widget):
        """
        initializes the maps api

        @param map_widget: the map widget to display the map
        """

        map_widget = map_widget
        map_widget.set_tile_server("http://localhost:8080/styles/maptiler-basic/" + str(MAP_TILE_RESOLUTION) + "/{z}/{x}/{y}.png", MAP_TILE_RESOLUTION)

    def geocode(self, query):
        """
        queries Nominatim for coordinate positions for a given point of interest

        @param query: the point of interest get the coordinates of

        @return: the json result of the query
        """

        try:
            results = get(
                NavigationAPI.NOMINATIM_URL, 
                params={"q": query}, 
                timeout=15
            ).json()
            return "Error Processing Request, Try Again..." if "error" in results else results

        # handles errors
        except:
            return "Error Processing Request, Try Again..."

    def navigate(self, p1, p2):
        """
        queries GraphHopper for navigation instructions between 2 points

        @param p1: the starting point
        @param p2: the ending point
            ** note: ordering matters **

        @return: the json response from GraphHopper
        """

        try:
            return get(
                NavigationAPI.GRAPH_HOPPER_URL,
                params= {
                    "point": [f"{p1[0]},{p1[1]}", f"{p2[0]},{p2[1]}"],
                    "profile": "car",
                    "points_encoded": "false"
                },
                timeout=15
            ).json()["paths"][0]

        except:
            pass
        