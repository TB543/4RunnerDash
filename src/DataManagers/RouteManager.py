from Connections.NavigationAPI import NavigationAPI
from shapely import STRtree, LineString, Point
from datetime import timedelta, datetime
from json import load, dump


class RouteManager:
    """
    a class to manage a route to a destination and announce instructions
    """

    # sets fields
    ANNOUNCEMENTS = {
        1609.344: "In 1 mile",  # note: keys here are in meters, ie 1609.344 meters is 1 mile
        304.8: "In 1000 feet"
    }

    # loads saved routes from file
    try:
        with open("AppData/routes.json", "r") as f:
            routes = load(f)
    except:
        routes = {"saved": {}}

    def __init__(self, name, lat, lon, audio_api):
        """
        creates the route object

        @param name: the name of the destination
        @param lat: the latitude of the destination
        @param lon: the longitude of the destination
        @param audio_api: the audio api for instruction tts
        """

        # fields
        self.name = name
        self.coords = (lat, lon)
        self.audio_api = audio_api
        navigation = NavigationAPI.navigate(self.coords)
        self.path = [(lat, lon) for lon, lat in navigation["points"]["coordinates"]]
        self.distance = navigation["distance"]
        self.time = navigation["time"]
        self.instructions = navigation["instructions"]
        self.instruction_index = -1

        # adds additional data to instructions to make update loop more efficient
        time_since_start = 0
        distance_since_start = 0
        for i, instruction in enumerate(self.instructions):
            instruction["announcements"] = set(RouteManager.ANNOUNCEMENTS.keys())
            instruction["time_since_start"] = time_since_start
            instruction["distance_since_start"] = distance_since_start
            time_since_start += instruction["time"]
            distance_since_start += instruction["distance"]

            # modifies the text to display the next instruction
            if i != len(self.instructions) - 1:
                instruction["sign"] = self.instructions[i + 1]["sign"]
                instruction["text"] = self.instructions[i + 1]["text"]
        self.instructions.pop()

        # creates objects for efficient coordinate "snapping"
        segments = []
        for instruction in self.instructions:
            interval = instruction["interval"]
            segment = LineString(self.path[interval[0]:interval[1] + 1]) if interval[0] != interval[1] else Point(*self.path[interval[0]])
            segments.append(segment)
        self.tree = STRtree(segments)

        # callback functions set on start
        self.gps_callback = None if not hasattr(self, "gps_callback") else self.gps_callback
        self.eta_callback = None
        self.time_callback = None
        self.miles_callback = None
        self.reroute_callback = None if not hasattr(self, "reroute_callback") else self.reroute_callback
        self.instruction_miles_callbacks = None

    def update_loop(self, coords):
        """
        the main update loop for the route manager, finds the current status of the route

        @param coords: the current coordinates on the route
        """

        # finds where the user is relative to the route
        point = Point(*coords)
        index = self.tree.nearest(point)
        segment = self.tree.geometries[index]
        instruction = self.instructions[index]
        offset = point.distance(segment)
        instruction_percent = segment.project(point) / segment.length if segment.geom_type == "LineString" else 1

        # handles when the user is too far off course
        if offset > .0006:
            self.__init__(self.name, *self.coords, self.audio_api)
            self.reroute_callback(True)
            return
        
        # does nothing if previous instruction is called (can happen due to gps accuracy)
        if index < self.instruction_index:
            return
        
        # updates the time 
        time_remaining = timedelta(milliseconds=self.time - ((instruction["time"] * instruction_percent) + instruction["time_since_start"]))
        self.eta_callback((datetime.now() + time_remaining).strftime("%I:%M %p"))
        self.time_callback(f"{int(time_remaining.total_seconds() / 3600)}:{int((time_remaining.total_seconds() % 3600) / 60):02d}")

        # updates miles
        distance_traveled = (instruction["distance"] * instruction_percent) + instruction["distance_since_start"]
        self.miles_callback(round((self.distance - distance_traveled) / 1609.344, 2))
        for instruction_loop, callback in zip(self.instructions, self.instruction_miles_callbacks):
            callback(round(((instruction_loop["distance"] + instruction_loop["distance_since_start"]) - distance_traveled) / 1609.344, 2))

        # announces the next instruction
        distance_left = instruction["distance"] * (1 - instruction_percent)
        announce = None
        if index > self.instruction_index:
            self.instruction_index = index
            announce = f"In {round(distance_left / 1609.344, 2)} miles"

        # checks if distance announcement threshold has been reached
        for distance, announcement in RouteManager.ANNOUNCEMENTS.items():
            if distance_left <= distance and instruction["distance"] > distance and distance in instruction["announcements"]:
                instruction["announcements"].remove(distance)
                announce = announcement

        # ensures only 1 announcement
        if announce:
            self.audio_api.tts_queue.put(f"{announce} {instruction['text']}.")

    def start(self, eta, time, miles, reroute, callbacks):
        """
        starts the route

        @param eta: the callback function for updating the ETA
        @param time: the callback function for updating the time remaining
        @param miles: the callback function for updating the miles remaining
        @param reroute: the callback function when a reroute is needed
        @param callbacks: a list of callbacks for updating the miles until each instruction
            ** note: all of these functions should take 1 parameter for the new value                   **
            ** the reroute callback will pass True as the parameter and modifies the current route data **

        @throws attribute error if already running
        """

        # starts the route
        self.eta_callback = eta
        self.time_callback = time
        self.miles_callback = miles
        self.reroute_callback = reroute
        self.instruction_miles_callbacks = callbacks
        self.update_loop(NavigationAPI.gps_coords)
        self.gps_callback = NavigationAPI.add_gps_callback(self.update_loop)

    def end(self):
        """
        ends the route or does nothing if the route has not been started
        """

        if self.gps_callback is not None:
            NavigationAPI.remove_gps_callback(self.gps_callback)
            self.delete(current_route=True) if "current" in RouteManager.routes else None
            self.gps_callback = None

    def save(self, name=None, current_route=False):
        """
        saves the route for quick access

        @param name: the name to save the route as (overrides current route name)
        @param current_route: a flag to determine if the route will persist across reboots
        """

        # saves route to dict
        name = name if name else self.name
        if current_route:
            RouteManager.routes["current"] = {"lat": self.coords[0], "lon": self.coords[1], "name": self.name}
        else:

            # ensures no duplicate names
            saved_name = name
            i = 1
            while saved_name in RouteManager.routes["saved"]:
                saved_name = f"{name} ({i})"
                i += 1
            RouteManager.routes["saved"][saved_name] = {"lat": self.coords[0], "lon": self.coords[1]}

        # writes to file
        with open("AppData/routes.json", "w") as f:
            dump(RouteManager.routes, f, indent=4)

    def delete(self, current_route=False):
        """
        deletes the route from the saved routes

        @param current_route: a flag to determine if the current route should be cleared
        """

        if current_route:
            RouteManager.routes.pop("current")
        else:
            RouteManager.routes["saved"].pop(self.name)
        with open("AppData/routes.json", "w") as f:
            dump(RouteManager.routes, f, indent=4)
