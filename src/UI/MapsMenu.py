from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkScrollableFrame, CTkLabel, CTkRadioButton, StringVar, DoubleVar
from UI.MapWidget import MapWidget
from Connections.NavigationAPI import NavigationAPI
from json import dumps, loads
from UI.VirtualKeyBoard import VirtualKeyboard
from DataManagers.RouteManager import RouteManager


class MapsMenu(CTkFrame):
    """
    map menu for the 4runner dashboard
    """

    # a dict of graphhopper signs and their text to display
    SIGNS = {
        -7: "⬉",  # keep left
        -3: "↰",  # turn sharp left
        -2: "←",  # turn left
        -1: "⤣",  # turn slight left
        0:  "↑",  # continue on street
        1:  "⤤",  # turn slight right
        2:  "→",  # turn right
        3:  "↱",  # turn sharp right
        4:  "⚑",  # finish
        5:  "⚐",  # via reached
        6:  "⥀",  # use roundabout
        7:  "⬈",  # keep right
    }

    def __init__(self, master, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.active_route = None

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
        focus_position_button = CTkButton(search_container, text="◉", width=12, font=("Arial", 20), command=lambda: self.map_widget.lock_position())
        self.search_entry = CTkEntry(search_container, placeholder_text="Enter Your Destination...", font=("Arial", 20), takefocus=0)
        search_button = CTkButton(search_container, text="Search", font=("Arial", 20), width=80, command=self.populate_search_results)
        search_container.pack(fill="x", padx=10)
        search_container.columnconfigure(1, weight=1)
        focus_position_button.grid(row=0, column=0)
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=5)
        search_button.grid(row=0, column=2)

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
        self.start_navigation_button.grid(row=0, column=0, sticky="ew", pady=(5, 0), padx=5)
        close.grid(row=0, column=1, sticky="ne", pady=(5, 0), padx=(0, 5))
        self.search_results_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.search_results_menu.rowconfigure(1, weight=1)
        self.search_results_menu.columnconfigure(0, weight=1)
        self.search_results_container.columnconfigure(1, weight=1)

        # creates the navigation menu
        self.navigation_menu = CTkFrame(map_container)
        self.end_navigation_button = CTkButton(self.navigation_menu, text="End Navigation", font=("Arial", 20), command=self.end_navigation)
        self.hide_navigation_button = CTkButton(self.navigation_menu, width=12, font=("Arial", 20))
        self.route_data = CTkFrame(self.navigation_menu, fg_color=map_container.cget("fg_color"))
        self.navigation_container = CTkScrollableFrame(self.navigation_menu, fg_color=self.navigation_menu.cget("fg_color"))

        # places the navigation menu and configures the grid
        self.hide_navigation_button.grid(row=0, column=0, rowspan=3, sticky="nsew", pady=5, padx=5)
        self.show_navigation_menu()
        self.navigation_menu.rowconfigure(2, weight=1)
        self.navigation_menu.columnconfigure(1, weight=1)
        self.navigation_container.columnconfigure(1, weight=1)

        # creates route data widgets
        self.route_eta = StringVar(self)
        self.route_time = StringVar(self)
        self.route_miles = DoubleVar(self)
        route_eta = CTkLabel(self.route_data, textvariable=self.route_eta, font=("Arial", 12, "bold"))
        route_time = CTkLabel(self.route_data, textvariable=self.route_time, font=("Arial", 12, "bold"))
        route_miles = CTkLabel(self.route_data, textvariable=self.route_miles, font=("Arial", 12, "bold"))
        route_eta_label = CTkLabel(self.route_data, text="ETA", font=("Arial", 10))
        route_time_label = CTkLabel(self.route_data, text="Time", font=("Arial", 10))
        route_miles_label = CTkLabel(self.route_data, text="Miles", font=("Arial", 10))

        # places route data widgets
        self.route_data.rowconfigure(0, weight=1)
        self.route_data.columnconfigure(0, weight=1, uniform="col")
        self.route_data.columnconfigure(1, weight=1, uniform="col")
        self.route_data.columnconfigure(2, weight=1, uniform="col")
        route_eta.grid(row=0, column=0, stick="s",)
        route_time.grid(row=0, column=1, stick="s")
        route_miles.grid(row=0, column=2, stick="s")
        route_eta_label.grid(row=1, column=0, stick="n")
        route_time_label.grid(row=1, column=1, stick="n")
        route_miles_label.grid(row=1, column=2, stick="n")
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

        self.active_route.end()
        self.navigation_menu.pack_forget()
        self.map_widget.delete_destination()

    def start_navigation(self, reroute=False):
        """
        starts the navigation to the selected waypoint

        @param reroute: determines if the current route needs to be rerouted
        """

        # handles reroute
        if reroute:
            self.map_widget.destination_path.delete()
            self.map_widget.destination_path = self.map_widget.set_path(self.active_route.path, color="#3E69CB")

        # starts the routing and displays route on UI
        self.active_route.end() if self.active_route else None
        self.active_route = self.map_widget.promote_POI() if not reroute else self.active_route

        # removes old instructions
        self.search_results_menu.pack_forget()
        self.navigation_menu.pack(side="right", fill="y", padx=(5, 0))
        self.show_navigation_menu() if not reroute else None
        for widget in self.navigation_container.winfo_children():
            widget.destroy()

        # populates the navigation container
        separator = None
        callbacks = []
        for row, instruction in enumerate(self.active_route.instructions):
            sign = CTkLabel(self.navigation_container, text=MapsMenu.SIGNS[instruction["sign"]], font=("Arial", 20))
            text = CTkLabel(self.navigation_container, text=instruction["text"], font=("Arial", 10), wraplength=120, justify="left")
            var = DoubleVar(self)
            miles = CTkLabel(self.navigation_container, textvariable=var, font=("Arial", 15))
            separator = CTkFrame(self.navigation_container, height=2)

            # function for placing widgets
            def place(s, t, m, p, r):
                if not s.winfo_ismapped():
                    s.grid(row=r * 2, column=0, sticky="ns")
                    t.grid(row=r * 2, column=1, sticky="w", padx=5)
                    m.grid(row=r * 2, column=2, sticky="ns")
                    p.grid(row=(r * 2) + 1, column=0, columnspan=3, sticky="ew", pady=5) if p.winfo_exists() else None

            # function for hiding the widgets
            def hide(s, t, m, p):
                if s.winfo_ismapped():
                    s.grid_forget()
                    t.grid_forget()
                    m.grid_forget()
                    p.grid_forget() if p.winfo_exists() else None
                    self.navigation_container._parent_canvas.yview_moveto(0)

            # ensures widgets get hidden if their mile value is negative (meaning instruction completed)
            callbacks.append(lambda m, v=var: self.after(0, lambda: v.set(m)))
            var.trace_add("write", lambda *args, v=var, s=sign, t=text, m=miles, p=separator, r=row: place(s, t, m, p, r) if v.get() >= 0 else hide(s, t, m, p))

        # clean up
        separator.destroy() if separator else None
        self.bind_focus(self.navigation_container)
        self.active_route.start(
            lambda e: self.after(0, lambda: self.route_eta.set(e)),
            lambda h: self.after(0, lambda: self.route_time.set(h)),
            lambda m: self.after(0, lambda: self.route_miles.set(m)),
            lambda r: self.after(0, lambda: self.start_navigation(r)),
            callbacks
        )

    def hide_navigation_menu(self):
        """
        hides the navigation menu
        """

        self.navigation_menu.grid_propagate(True)
        self.navigation_container.grid_forget()
        self.route_data.grid_forget()
        self.end_navigation_button.grid_forget()
        self.hide_navigation_button.configure(text="◂", command=self.show_navigation_menu)

    def show_navigation_menu(self):
        """
        displays the navigation menu
        """

        self.navigation_menu.grid_propagate(False)
        self.navigation_menu.configure(width=250)
        self.end_navigation_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=(0, 5))
        self.route_data.grid(row=1, column=1, sticky="nsew", padx=(0, 5), pady=(0, 5))
        self.navigation_container.grid(row=2, column=1, sticky="nsew", padx=(0, 5), pady=(0, 5))
        self.hide_navigation_button.configure(text="▸", command=self.hide_navigation_menu)

    def select_search_result(self):
        """
        updates the UI when the user selects a search result
        """

        # handles no route found 
        waypoint = loads(self.selected_waypoint.get())
        if not (navigation := NavigationAPI.navigate((float(waypoint["lat"]), float(waypoint["lon"])))):
            return

        # updates UI with selected search result
        route = RouteManager(float(waypoint["lat"]), float(waypoint["lon"]), waypoint["display_name"], navigation)
        self.start_navigation_button.configure(state="normal")
        self.map_widget.set_POI(route)

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
        results = NavigationAPI.geocode(self.search_entry.get())
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
            label = CTkLabel(self.search_results_container, text=result["display_name"], font=("Arial", 10), wraplength=185, justify="left")
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

        self.map_widget.delete_POI()
        self.search_results_menu.pack_forget()
        self.navigation_menu.pack(side="right", fill="y", padx=(5, 0)) if self.active_route else None

    def destroy(self):
        """
        overrides the destroy method to also shut down the NavigationAPI connection
        """

        NavigationAPI.shutdown(self)
        super().destroy()
