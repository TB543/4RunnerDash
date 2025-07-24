from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkScrollableFrame, CTkLabel, CTkRadioButton, StringVar
from UI.MapWidget import MapWidget
from Connections.NavigationAPI import NavigationAPI
from json import dumps, loads


class MapsMenu(CTkFrame):
    """
    map menu for the 4runner dashboard
    """

    def __init__(self, master, appearance_manager, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param appearance_manager: a reference to the apps appearance manager
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.appearance_manager = appearance_manager

        # creates spacer widgets and sets grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = CTkButton(self, text="", font=("Arial", 100), fg_color="transparent", hover=False, height=0)
            spacer.grid(row=1, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates top level widgets
        main_menu = CTkButton(self, text="Main Menu", font=("Arial", 20), command=lambda: master.change_menu("main"))
        container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        container.grid(row=1, column=1, columnspan=7, sticky="nsew", pady=10)

        # creates search container
        search_container = CTkFrame(container, fg_color=self.cget("fg_color"))
        self.search_entry = CTkEntry(search_container, placeholder_text="Enter Your Destination...", font=("Arial", 20))
        self.search_entry._is_focused = False
        search_button = CTkButton(search_container, text="Search", font=("Arial", 20), width=80, command=self.search)
        search_container.pack(fill="x", padx=10)
        self.search_entry.pack(side="left", fill="x", expand=True)
        search_button.pack(side="right", padx=(5, 0))

        # creates map container
        map_container = CTkFrame(container, fg_color=self.cget("fg_color"))
        self.map_widget = MapWidget(map_container, corner_radius=12)
        map_container.pack(fill="both", expand=True, padx=10, pady=(3, 0))
        self.map_widget.pack(side="left", fill="both", expand=True)
        self.selected_waypoint = StringVar(self)

        # loads api and creates search results container
        self.api = NavigationAPI(self.map_widget)
        self.search_results_popup = CTkFrame(map_container)
        self.start_navigation_button = CTkButton(self.search_results_popup, text="Start Navigation", font=("Arial", 20), command=self.start_navigation)
        close = CTkButton(self.search_results_popup, text="x", width=12, font=("Arial", 20), command=self.search_results_popup.pack_forget)
        self.search_results_container = CTkScrollableFrame(self.search_results_popup, fg_color=self.search_results_popup.cget("fg_color"))

        # places the search results container and configures the grid
        self.start_navigation_button.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        close.grid(row=0, column=1, sticky="ne", pady=5, padx=(0, 5))
        self.search_results_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=(0, 2))
        self.search_results_popup.rowconfigure(1, weight=1)
        self.search_results_popup.columnconfigure(0, weight=1)
        self.search_results_container.columnconfigure(1, weight=1)

        # creates map markers for the map
        self.position_marker = self.map_widget.set_position(*NavigationAPI.GPS_COORDS, "You", True, text_color="#87CEFA", marker_color_circle="white", marker_color_outside="#1E90FF")
        self.search_marker = None
        self.navigation_marker = None

    def start_navigation(self):
        """
        starts the navigation to the selected waypoint
        """

        # draws the path to the map
        self.search_marker.delete()
        self.navigation_marker = self.map_widget.set_marker(*self.search_marker.position, self.search_marker.text, text_color="#9B261E", marker_color_circle="white", marker_color_outside="#C5542D")
        navigation = self.api.navigate(self.position_marker.position, self.navigation_marker.position)
        self.map_widget.set_path([(lat, lon) for lon, lat in navigation["points"]["coordinates"]])

        # loads the directions
        dist = navigation["distance"]
        time = navigation["time"]
        instructions = navigation["instructions"]

    def set_waypoint(self):
        """
        places a marker at the selected location on the map for the user to see and fits the map to show the users
        location and the waypoint
        """

        # configures markers
        self.start_navigation_button.configure(state="normal")
        self.search_marker.delete() if self.search_marker else None
        waypoint = loads(self.selected_waypoint.get())
        self.search_marker = self.map_widget.set_marker(float(waypoint["lat"]), float(waypoint["lon"]), waypoint["display_name"], text_color="#FFD580", marker_color_circle="white", marker_color_outside="#FFA500")
        
        # repositions map
        lat1, lon1 = self.position_marker.position
        lat2, lon2 = self.search_marker.position
        self.map_widget.fit_bounding_box((max(lat1, lat2), min(lon1, lon2)), (min(lat1, lat2), max(lon1, lon2)))
        self.map_widget.after(100, lambda: self.map_widget.set_zoom(self.map_widget.zoom - 1))

    def search(self):
        """
        handles when the user presses the search button
        """

        # clears old results
        self.focus()
        self.selected_waypoint.set("")
        self.search_results_popup.pack(side="right", fill="y", padx=(5, 0))
        self.start_navigation_button.configure(state="disabled")
        self.search_marker.delete() if self.search_marker else None
        for widget in self.search_results_container.winfo_children():
            widget.destroy()

        # handles when results contains an error
        results = self.api.geocode(self.search_entry.get())
        if isinstance(results, str):
            label = CTkLabel(self.search_results_container, text=results, font=("Arial", 10))
            label.grid(row=0, column=1)
            return

        # handles when no results are found
        if not results:
            label = CTkLabel(self.search_results_container, text="No Results Found...", font=("Arial", 10))
            label.grid(row=0, column=1)

        # draws results to screen
        separator = None
        for row, result in enumerate(results):
            button = CTkRadioButton(self.search_results_container, text="", width=10, variable=self.selected_waypoint, value=dumps(result), command=self.set_waypoint)
            label = CTkLabel(self.search_results_container, text=result["display_name"], font=("Arial", 10), wraplength=165, justify="left")
            separator = CTkFrame(self.search_results_container, height=2)
            button.grid(row=row * 2, column=0, sticky="ns")
            label.grid(row=row * 2, column=1, sticky="w")
            separator.grid(row=(row * 2) + 1, column=0, columnspan=2, sticky="ew", pady=5)

        # destroys the bottom separator and clears the text input
        separator.destroy() if separator else None
        self.search_entry.delete(0, "end")
