from tkintermapview import TkinterMapView
from tkintermapview import convert_address_to_coordinates  # todo test offline


class MapWidget(TkinterMapView):
    """
    a subclass of TkinterMapView with pi touch screen support

    todo cache requests
    """


# from customtkinter import CTk
# root = CTk()
# map = MapWidget(root)
# map.pack(fill="both", expand=True)
# map.set_tile_server("http://localhost:8080/styles/test-style/256/{z}/{x}/{y}.png")
# root.mainloop()
