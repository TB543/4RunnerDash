from AppData import MAP_TILE_RESOLUTION, INITIAL_MAP_COORDS
from requests import get
from serial import Serial
from threading import Thread
from sys import argv
from time import sleep
from math import atan2, degrees
from json import load, dump
try:
    from bmm150 import BMM150, PresetMode
except ModuleNotFoundError:
    from Dev.Imports.bmm150 import *


class NavigationAPI:
    """
    a class to communicate with various mapping services:
        -> GraphHopper connection for routing       port: 8989
        -> TileServer-GL connection for map tiles   port: 8080
        -> Nominatim connection for geocoding       port: 8088
        -> GPS module for location                  port: /dev/ttyAMA0
        -> Compass module for dead reckoning        port: i2c
    """

    @staticmethod
    def get_heading():
        """
        gets the heading from the compass module

        @return the heading the degrees
        """

        x, y, z = NavigationAPI.compass.read_mag_data()
        return degrees(atan2(x, y))

    @staticmethod
    def gps_read_loop():
        """
        reads the gps data and updates the gps coords attribute of the class
        """

        # attempts to open gps serial port, defaults to dev mode if fails
        try:
            gps = Serial("/dev/ttyAMA0")
        except:
            gps = None

        # changes coords to global initial coords when in dev mode
        while ((not gps) and NavigationAPI.running) or (len(argv) == 2 and argv[1] == "dev" and NavigationAPI.running):
            sleep(1)
            for callback in NavigationAPI.callbacks[:]:
                try:
                    NavigationAPI.gps_coords = INITIAL_MAP_COORDS
                    callback(NavigationAPI.gps_coords)
                except:
                    continue

        # reads from the gps module
        while NavigationAPI.running:
            line = gps.readline().decode('ascii', errors='ignore').strip().split(",") if gps.in_waiting > 0 else sleep(1)
            if line and line[0] == "$GPRMC" and line[2] == "A":

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
                for callback in NavigationAPI.callbacks[:]:  # copy so that race conditions do not occur
                    try:
                        callback(NavigationAPI.gps_coords)
                    except:
                        continue

        if gps:
            gps.close()

    # class fields
    GRAPH_HOPPER_URL = "http://localhost:8989/route"
    compass = BMM150(PresetMode.HIGHACCURACY)
    callbacks = []
    thread = Thread(target=gps_read_loop, daemon=True)
    running = True

    # use internet for apis when in debug mode
    if len(argv) == 2 and argv[1] == "dev":
        TILE_SERVER_URL = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    # otherwise use localhost running apis
    else:
        TILE_SERVER_URL = "http://localhost:8080/styles/maptiler-basic/" + str(MAP_TILE_RESOLUTION) + "/{z}/{x}/{y}.png"
        NOMINATIM_URL = "http://localhost:8088/search"

    # attempts to read previous gps coords from file
    try:
        with open("AppData/gps.json", "r") as f:
            gps_coords = load(f)["coords"]
    except:
        gps_coords = (0, 0)

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
                    "q": query,
                    "format": "jsonv2",
                },
                headers={
                    "User-Agent": "4RunnerDash"
                },
                timeout=15
            ).json()
            return "Error Processing Request, Try Again..." if "error" in results or isinstance(results, dict) else results

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
                params={
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

        # writes coords to file
        with open("AppData/gps.json", "w") as f:
            dump({"coords": cls.gps_coords}, f, indent=4)

        # shuts down gps read thread
        cls.running = False
        while cls.thread.is_alive():
            root.update()
