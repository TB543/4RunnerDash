from tkintermapview import TkinterMapView


class MapWidget(TkinterMapView):
    """
    a subclass of TkinterMapView with pi touch screen support
    """

    def __init__(self, master, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
