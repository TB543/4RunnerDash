from Connections.NavigationAPI import NavigationAPI


class RouteManager:
    """
    a class to manage a route to a destination
    """

    def __init__(self, lat, lon, name, path, distance, time, instructions):
        """
        creates the route object

        @param lat: the latitude of the destination
        @param lon: the longitude of the destination
        @param name: the name of the destination
        @param path: a list of points to create the path to the destination in geojson format
        @param distance: the distance to the destination
        @param time: the time it will take to travel to the destination
        @param instructions: a list of instructions for traveling to the destination
        """

        # fields
        self.coords = (lat, lon)
        self.name = name
        self.path = [(lat, lon) for lon, lat in path]
        self.distance = distance
        self.time = time
        self.instructions = instructions

        # callback functions set on start
        self.gps_callback = None
        self.eta_callback = None
        self.time_callback = None
        self.miles_callback = None
        self.instruction_miles_callbacks = None

    def update_loop(self, coords):
        """
        the main update loop for the route manager, finds the current status of the route

        @param coords: the current coordinates on the route
        """

        print(coords)

    def start(self, eta, time, miles, callbacks):
        """
        starts the route

        @param eta: the callback function for updating the ETA
        @param time: the callback function for updating the time remaining
        @param miles: the callback function for updating the miles remaining
        @param callbacks: a list of callbacks for updating the miles until each instruction
            ** note: all of these functions should take 1 parameter for the new value **

        @throws attribute error if already running
        """

        # handles when route is already running
        if self.gps_callback is not None:
            raise AttributeError("Route Already Started")

        # starts the route
        self.eta_callback = eta
        self.time_callback = time
        self.miles_callback = miles
        self.instruction_miles_callbacks = callbacks
        self.gps_callback = NavigationAPI.add_gps_callback(self.update_loop)
        self.update_loop(NavigationAPI.gps_coords)

    def end(self):
        """
        ends the route or does nothing if the route has not been started
        """

        if self.gps_callback is not None:
            NavigationAPI.remove_gps_callback(self.gps_callback)
            self.gps_callback = None
        