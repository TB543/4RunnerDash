from datetime import timedelta


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
        self.eta_callback = None
        self.time_callback = None
        self.miles_callback = None

    def start(self, eta, time, miles):
        """
        starts the route

        @param eta: the callback function for updating the ETA
        @param time: the callback function for updating the time remaining
        @param miles: the callback function for updating the miles remaining
        """

        self.eta_callback = eta
        self.time_callback = time
        self.miles_callback = miles

    def end(self):
        """
        ends the route
        """
        