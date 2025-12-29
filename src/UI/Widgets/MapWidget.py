from tkintermapview import TkinterMapView
from customtkinter import AppearanceModeTracker
from AppData import INITIAL_MAP_COORDS, INITIAL_MAP_ZOOM, MAP_TILE_RESOLUTION
from sys import argv


class MapWidget(TkinterMapView):
    """
    a subclass of TkinterMapView with pi touch screen support
    """

    def __init__(self, master, **kwargs):
        """
        overrides the init method to remove the zoom control buttons

        @param master: the parent widget
        @param kwargs: additional keyword arguments for TkinterMapView
        """

        # configures superclass
        super().__init__(master, **kwargs)
        AppearanceModeTracker.add(self.update_appearance_mode)
        self.canvas.bind("<B1-Motion>", lambda e: setattr(self, "follow_position", False), add="+")
        for button in self.canvas.find_withtag("button"):
            self.canvas.tag_unbind(button, "<Enter>")
            self.canvas.tag_unbind(button, "<Leave>")

        # creates fields and sets map position
        self.tile_servers = None
        self.position_marker = None
        self.POI_marker = None
        self.destination_marker = None
        self.POI_path = None
        self.destination_path = None
        self.follow_position = True
        self.pending_route = None
        self.set_zoom(INITIAL_MAP_ZOOM)
        self.set_position(*INITIAL_MAP_COORDS)

        # allows right click to change coords when in dev mode
        if len(argv) == 2 and argv[1] == "dev":
            self.add_right_click_menu_command("Set Coords", lambda coords: INITIAL_MAP_COORDS.__setitem__(slice(None), coords), pass_coords=True)

    def delete_destination(self):
        """
        deletes the current destination and path
        """

        self.destination_marker.delete() if self.destination_marker else None
        self.destination_path.delete() if self.destination_path else None

    def promote_POI(self):
        """
        changes the selected point of interest to a destination and
        draws the path between the current location and the destination

        @return the route for the POI that was pending
        """

        self.delete_destination()
        self.delete_POI()
        self.destination_marker = self.set_marker(*self.POI_marker.position, self.POI_marker.text, text_color="#9B261E", marker_color_circle="white", marker_color_outside="#C5542D")
        self.destination_path = self.set_path(self.POI_path.position_list, color="#3E69CB")
        self.lock_position()
        return self.pending_route

    def set_POI(self, route):
        """
        sets a point of interest marker on the map and zooms the map
        to fit the POI and the user position

        @param route: the route object for the POI
        """

        # creates marker and path
        self.pending_route = route
        self.delete_POI()
        self.POI_marker = self.set_marker(*route.coords, route.name, text_color="#FFD580", marker_color_circle="white", marker_color_outside="#FFA500")
        self.POI_path = self.set_path(route.path, color="#668ADF")
        
        # repositions map
        self.unlock_position()
        if self.position_marker:
            lat1, lon1 = self.position_marker.position
            lat2, lon2 = self.POI_marker.position
            self.fit_bounding_box((max(lat1, lat2), min(lon1, lon2)), (min(lat1, lat2), max(lon1, lon2)))
            self.after(100, lambda: self.set_zoom(self.zoom - 1))
        else:
            self.set_position(*route.coords)

    def delete_POI(self):
        """
        removed the current POI marker and path

        ** note: there is a known glitch here when user clicks a search result while another one is busy loading
            it will fail to delete the old marker/path. This is a glitch within TkinterMapView **
        """

        self.POI_marker.delete() if self.POI_marker else None
        self.POI_path.delete() if self.POI_path else None

    def lock_position(self):
        """
        locks the map onto the users position
        """

        self.follow_position = True
        self.set_position(*self.position_marker.position) if self.position_marker else None

    def unlock_position(self):
        """
        stops following the users position
        """

        self.follow_position = False

    def update_position(self, coords):
        """
        updates the coordinates of the position marker

        @param coords: the new coordinates for the position marker
        """

        # updates position marker
        if not self.position_marker:
            self.position_marker = self.set_marker(*coords, "You", text_color="#87CEFA", marker_color_circle="white", marker_color_outside="#1E90FF")
        self.position_marker.set_position(*coords)

        # sets position if following
        if self.follow_position:
            self.set_position(*coords)

    def set_tile_servers(self, tile_server_urls):
        """
        slightly different from the superclass method to allow multiple tile servers
        for different appearance modes 

        @param tile_server_urls: a tuple of tile server urls for light and dark modes respectively
        """

        self.tile_servers = tile_server_urls
        self.update_appearance_mode("Light" if AppearanceModeTracker.get_mode() == 0 else "Dark")

    def update_appearance_mode(self, mode):
        """
        updates the appearance mode of the widget

        @param mode: the new appearance mode
        """

        self.bg_color = self.master._apply_appearance_mode(self.master.cget("fg_color"))
        self.draw_rounded_corners()
        self.set_tile_server(self.tile_servers[0] if mode == "Light" else self.tile_servers[1], MAP_TILE_RESOLUTION)
