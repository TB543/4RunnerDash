from AppData import MAP_TILE_RESOLUTION, INITIAL_MAP_COORDS
from requests import get
from serial import Serial
from threading import Thread
from sys import argv


class NavigationAPI:
    """
    a class to communicate with various mapping services:
        -> GraphHopper connection for routing       port: 8989
        -> TileServer-GL connection for map tiles   port: 8080
        -> Nominatim connection for geocoding       port: 8088
        -> BN-220 GPS module for location           port: /dev/ttyAMA0
    """

    @staticmethod
    def gps_read_loop():
        """
        reads the gps data and updates the gps coords attribute of the class
        """

        # reads from the gps module
        gps = Serial("/dev/ttyAMA0")
        while NavigationAPI.running:
            line = gps.readline().decode('ascii', errors='ignore').strip().split(",")
            if len(line) == 13 and line[0] == "$GNRMC" and line[2] == "A" and len(argv) == 1:
                
                # reads the useful data
                lat = line[3]
                lat_dir = line[4]
                lon = line[5]
                lon_dir = line[6]

                # converts lat lon to coordinates
                lat = int(lat[:2]) + float(lat[2:]) / 60
                lon = int(lon[:3]) + float(lon[3:]) / 60
                NavigationAPI.gps_coords = (-lat if lat_dir == 'S' else lat, -lon if lon_dir == 'W' else lon)

                # sends new GPS coords via callback functions
                for callback in NavigationAPI.callbacks[:]:
                    try:
                        callback(NavigationAPI.gps_coords)
                    except:
                        continue
            
            # changes coords to global initial coords when in dev mode
            elif len(argv) == 2 and argv[1] == "dev":
                for callback in NavigationAPI.callbacks[:]:
                    try:
                        NavigationAPI.gps_coords = INITIAL_MAP_COORDS
                        callback(NavigationAPI.gps_coords)
                    except:
                        continue

        gps.close()

    TILE_SERVER_URL = "http://localhost:8080/styles/maptiler-basic/" + str(MAP_TILE_RESOLUTION) + "/{z}/{x}/{y}.png"
    NOMINATIM_URL = "http://localhost:8088/search"
    GRAPH_HOPPER_URL = "http://localhost:8989/route"
    gps_coords = (0, 0)
    callbacks = []
    thread = Thread(target=gps_read_loop, daemon=True)
    running = True

    def __init__(self, map_widget):
        """
        initializes the maps api

        @param map_widget: the map widget to display the map
        """

        map_widget = map_widget
        map_widget.set_tile_server(NavigationAPI.TILE_SERVER_URL, MAP_TILE_RESOLUTION)
        if not NavigationAPI.thread.is_alive():
            NavigationAPI.thread.start()

    @staticmethod
    def geocode(query):
        """
        queries Nominatim for coordinate positions for a given point of interest

        @param query: the point of interest get the coordinates of

        @return: the json result of the query
        """

        try:
            results = get(
                NavigationAPI.NOMINATIM_URL, 
                params={
                    "q": query
                }, 
                timeout=15
            ).json()
            return "Error Processing Request, Try Again..." if "error" in results or isinstance(results, dict)  else results

        # handles errors
        except:
            return "Error Processing Request, Try Again..."

    @classmethod
    def navigate(cls, point):
        """
        queries GraphHopper for navigation instructions between current location and
        the given point

        @param point: the ending point

        @return: the json response from GraphHopper
        """

        try:
            return get(
                NavigationAPI.GRAPH_HOPPER_URL,
                params= {
                    "point": [f"{cls.gps_coords[0]},{cls.gps_coords[1]}", f"{point[0]},{point[1]}"],
                    "profile": "car",
                    "points_encoded": "false"
                },
                timeout=15
            ).json()["paths"][0]

        except:
            pass

    @classmethod
    def add_gps_callback(cls, callback):
        """
        adds a callback function when the GPS position updates

        @param callback: the function to call when the GPS position updates
            this function should take 2 parameter, a tuple for the coordinates

        @return: the index of the gps callback, used later in removing the callback 
        """

        cls.callbacks.append(callback)
        return len(cls.callbacks) - 1

    @classmethod
    def remove_gps_callback(cls, index):
        """
        removes a callback when the GPS position updates

        @param index: the index of the callback (given from add_gps_callback)
        """

        cls.callbacks.pop(index)

    @classmethod
    def shutdown(cls, root):
        """
        shuts down the gps connection

        @param root: the root window to update to ensure
            callbacks are processed while shutting down
        """

        cls.running = False
        while cls.thread.is_alive():
            root.update()
