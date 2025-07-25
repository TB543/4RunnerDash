from tkintermapview import TkinterMapView
from customtkinter import AppearanceModeTracker
from AppData import INITIAL_MAP_COORDS, INITIAL_MAP_ZOOM


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
        for button in self.canvas.find_withtag("button"):
            self.canvas.tag_unbind(button, "<Enter>")
            self.canvas.tag_unbind(button, "<Leave>")

        # creates fields and sets map position
        self.position_marker = None
        self.POI_marker = None
        self.destination_marker = None
        self.follow_position = True
        self.set_zoom(INITIAL_MAP_ZOOM)
        self.set_position(*INITIAL_MAP_COORDS)

    def delete_destination(self):
        """
        deletes the current destination and path
        """

        self.delete_all_path()
        self.destination_marker.delete() if self.destination_marker else None

    def promote_POI(self, path):
        """
        changes the selected point of interest to a destination and
        draws the path between the current location and the destination

        @param path: the list of positions between the 2 points in geojson format
        """

        self.POI_marker.delete()
        self.destination_marker = self.set_marker(*self.POI_marker.position, self.POI_marker.text, text_color="#9B261E", marker_color_circle="white", marker_color_outside="#C5542D")
        self.set_path([(lat, lon) for lon, lat in path])

    def set_POI(self, x, y, name):
        """
        sets a point of interest marker on the map and zooms the map
        to fit the POI and the user position

        @param x: the x coordinate of the marker
        @param y: the y coordinate of the marker
        @param name: the name of the marker
        """

        # creates marker
        self.POI_marker.delete() if self.POI_marker else None
        self.POI_marker = self.set_marker(x, y, name, text_color="#FFD580", marker_color_circle="white", marker_color_outside="#FFA500")
        
        # repositions map
        if self.position_marker:
            lat1, lon1 = self.position_marker.position
            lat2, lon2 = self.POI_marker.position
            self.fit_bounding_box((max(lat1, lat2), min(lon1, lon2)), (min(lat1, lat2), max(lon1, lon2)))
            self.after(100, lambda: self.set_zoom(self.zoom - 1))
        else:
            self.set_position(x, y)

    def delete_POI(self):
        """
        removed the current POI marker
        """

        self.POI_marker.delete() if self.POI_marker else None

    def update_position(self, coords):
        """
        updates the coordinates of the position marker

        @param coords: the new coordinates for the position marker
        """

        if not self.position_marker:
            self.position_marker = self.set_marker(*coords, "You", text_color="#87CEFA", marker_color_circle="white", marker_color_outside="#1E90FF")
        self.position_marker.set_position(*coords)

        if self.follow_position:
            self.set_position(*coords)

    def update_appearance_mode(self, mode):
        """
        updates the appearance mode of the widget

        @param mode: the new appearance mode
        """

        self.bg_color = self.master._apply_appearance_mode(self.master.cget("fg_color"))
        self.draw_rounded_corners()
