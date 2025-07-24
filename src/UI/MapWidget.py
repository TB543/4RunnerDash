from tkintermapview import TkinterMapView
from customtkinter import AppearanceModeTracker


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

    def update_appearance_mode(self, mode):
        """
        updates the appearance mode of the widget

        @param mode: the new appearance mode
        """

        self.bg_color = self.master._apply_appearance_mode(self.master.cget("fg_color"))
        self.draw_rounded_corners()

    def set_address(self, *args, **kwargs):
        """
        this method will not be used and will not work offline

        @param args: the arguments for the superclass
        @param kwargs: the keyword arguments for the superclass

        @throws AttributeError: if attempted to call
        """

        raise AttributeError("Geocoding for MapWidget not supported. Use MapsAPI")
