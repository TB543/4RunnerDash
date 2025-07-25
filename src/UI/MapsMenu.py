from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkScrollableFrame, CTkLabel, CTkRadioButton, StringVar
from UI.MapWidget import MapWidget
from Connections.NavigationAPI import NavigationAPI
from json import dumps, loads
from UI.VirtualKeyBoard import VirtualKeyboard


class MapsMenu(CTkFrame):
    """
    map menu for the 4runner dashboard
    """

    def __init__(self, master, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.navigating = False

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
        self.search_entry = CTkEntry(search_container, placeholder_text="Enter Your Destination...", font=("Arial", 20), takefocus=0)
        search_button = CTkButton(search_container, text="Search", font=("Arial", 20), width=80, command=self.populate_search_results)
        search_container.pack(fill="x", padx=10)
        self.search_entry.pack(side="left", fill="x", expand=True)
        search_button.pack(side="right", padx=(5, 0))

        # configures search entry settings and adds a virtual keyboard for it
        self.search_entry._is_focused = False
        self.search_entry._entry.configure(cursor="none")
        self.keyboard = VirtualKeyboard(self, self.search_entry, self.populate_search_results)

        # creates map container
        map_container = CTkFrame(container, fg_color=self.cget("fg_color"))
        self.map_widget = MapWidget(map_container, corner_radius=12)
        map_container.pack(fill="both", expand=True, padx=10, pady=(3, 0))
        self.map_widget.pack(side="left", fill="both", expand=True)
        self.selected_waypoint = StringVar(self)

        # loads api
        self.api = NavigationAPI(self.map_widget)
        NavigationAPI.add_gps_callback(lambda coords: self.after(0, lambda: self.map_widget.update_position(coords)))

        # creates search results menu
        self.search_results_menu = CTkFrame(map_container, width=250)
        self.start_navigation_button = CTkButton(self.search_results_menu, text="Start Navigation", font=("Arial", 20), command=self.start_navigation)
        close = CTkButton(self.search_results_menu, text="x", width=12, font=("Arial", 20), command=self.close_search_menu)
        self.search_results_container = CTkScrollableFrame(self.search_results_menu, fg_color=self.search_results_menu.cget("fg_color"))

        # places the search results menu and configures the grid
        self.search_results_menu.grid_propagate(False)
        self.start_navigation_button.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        close.grid(row=0, column=1, sticky="ne", pady=5, padx=(0, 5))
        self.search_results_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=(0, 2))
        self.search_results_menu.rowconfigure(1, weight=1)
        self.search_results_menu.columnconfigure(0, weight=1)
        self.search_results_container.columnconfigure(1, weight=1)

        # creates the navigation menu
        self.navigation_menu = CTkFrame(map_container)
        self.end_navigation_button = CTkButton(self.navigation_menu, text="End Navigation", font=("Arial", 20), command=self.end_navigation)
        self.hide_navigation_button = CTkButton(self.navigation_menu, width=12, font=("Arial", 20))
        self.navigation_container = CTkScrollableFrame(self.navigation_menu, fg_color=self.navigation_menu.cget("fg_color"))

        # places the navigation menu and configures the grid
        self.hide_navigation_button.grid(row=0, column=0, rowspan=2, sticky="ns", pady=5, padx=5)
        self.show_navigation_menu()
        self.navigation_menu.rowconfigure(1, weight=1)
        self.navigation_menu.columnconfigure(1, weight=1)
        self.navigation_container.columnconfigure(1, weight=1)
        self.bind_focus(self)

    def bind_focus(self, root):
        """
        recursively ensures that every element gains focus when it is clicked so entry can be clicked out of 
        """

        root.bind("<Button-1>", lambda e: self.focus(), add="+")
        for widget in root.winfo_children():
            if widget != self.keyboard and widget != self.search_entry:
                self.bind_focus(widget)

    def end_navigation(self):
        """
        ends the current navigation
        """

        self.navigating = False
        self.navigation_menu.pack_forget()
        self.map_widget.delete_destination()

    def start_navigation(self):
        """
        starts the navigation to the selected waypoint
        """

        # handles no route found 
        waypoint = loads(self.selected_waypoint.get())
        navigation = self.api.navigate(NavigationAPI.GPS_COORDS, (float(waypoint["lat"]), float(waypoint["lon"])))
        if not navigation:
            return

        # ends previous navigation
        if self.navigating:
            self.end_navigation()

        # adds path to the map
        self.navigating = True
        self.map_widget.promote_POI(navigation["points"]["coordinates"])

        # populates the navigation widgets
        self.search_results_menu.pack_forget()
        self.navigation_menu.pack(side="right", fill="y", padx=(5, 0))
        self.show_navigation_menu()

        # loads the directions
        dist = navigation["distance"]
        time = navigation["time"]
        instructions = navigation["instructions"]

    def hide_navigation_menu(self):
        """
        hides the navigation menu
        """

        self.navigation_menu.grid_propagate(True)
        self.navigation_container.grid_forget()
        self.end_navigation_button.grid_forget()
        self.hide_navigation_button.configure(text="◂", command=self.show_navigation_menu)

    def show_navigation_menu(self):
        """
        displays the navigation menu
        """

        self.navigation_menu.grid_propagate(False)
        self.navigation_menu.configure(width=250)
        self.end_navigation_button.grid(row=0, column=1, sticky="ew", pady=5, padx=(0, 5))
        self.navigation_container.grid(row=1, column=1, sticky="nsew", padx=2, pady=(0, 2))
        self.hide_navigation_button.configure(text="▸", command=self.hide_navigation_menu)

    def select_search_result(self):
        """
        updates the UI when the user selects a search result
        """

        self.start_navigation_button.configure(state="normal")
        waypoint = loads(self.selected_waypoint.get())
        self.map_widget.set_POI(float(waypoint["lat"]), float(waypoint["lon"]), waypoint["display_name"])

    def populate_search_results(self):
        """
        handles when the user presses the search button
        """

        # clears old results
        self.navigation_menu.pack_forget()
        self.selected_waypoint.set("")
        self.search_results_menu.pack(side="right", fill="y", padx=(5, 0))
        self.start_navigation_button.configure(state="disabled")
        self.map_widget.delete_POI()
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
            button = CTkRadioButton(self.search_results_container, text="", width=10, variable=self.selected_waypoint, value=dumps(result), command=self.select_search_result)
            label = CTkLabel(self.search_results_container, text=result["display_name"], font=("Arial", 10), wraplength=165, justify="left")
            label.bind("<Button-1>", lambda e, btn=button: btn.invoke())
            separator = CTkFrame(self.search_results_container, height=2)
            button.grid(row=row * 2, column=0, sticky="ns")
            label.grid(row=row * 2, column=1, sticky="w")
            separator.grid(row=(row * 2) + 1, column=0, columnspan=2, sticky="ew", pady=5)

        # clean up
        separator.destroy() if separator else None
        self.search_entry.delete(0, "end")
        self.bind_focus(self.search_results_container)

    def close_search_menu(self):
        """
        closes the search menu popup
        """

        self.map_widget.POI_marker.delete() if self.map_widget.POI_marker else None
        self.search_results_menu.pack_forget()
        self.navigation_menu.pack(side="right", fill="y", padx=(5, 0)) if self.navigating else None

    def destroy(self):
        """
        overrides the destroy method to also shut down the NavigationAPI connection
        """

        NavigationAPI.shutdown(self)
        super().destroy()
