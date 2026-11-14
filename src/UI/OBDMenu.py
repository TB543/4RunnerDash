from customtkinter import CTkFrame, CTkLabel, DoubleVar, StringVar, CTkScrollableFrame, set_widget_scaling
from Dev.TSCTkButton import TSCTkButton
from Dev.PWCTkButton import PWCTkButton
from DataManagers.MileManager import MileManger
from DataManagers.DateManager import DateManager
from UI.Widgets.Calendar import Calendar
from threading import Thread


class OBDMenu(CTkFrame):
    """
    OBD scanner menu for the 4runner dashboard
    """

    def __init__(self, master, appearance_manager, job_manager, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param appearance_manager: a reference to the apps appearance manager
        @param job_manager: a class for managing jobs for connecting to the obd interface
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.appearance_manager = appearance_manager
        self.job_manager = job_manager

        # creates spacer widgets and sets grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = TSCTkButton(self, text="", font=("Arial", 100), fg_color="transparent", hover=False, height=0)
            spacer.grid(row=1, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates toplevel widgets
        main_menu = TSCTkButton(self, text="Main Menu", font=("Arial", 20), command=lambda: master.change_menu("main"))
        get_codes_button = TSCTkButton(self, text="Get Codes", font=("Arial", 20), command=self.get_codes)
        container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        get_codes_button.grid(row=2, column=1, columnspan=7, pady=(0, 10), sticky="sew")
        container.grid(row=1, column=1, columnspan=7, sticky="nsew", pady=10)

        # creates vars to hold obd data and binds them to the API
        mpg = DoubleVar(self)
        self.api = None
        self.api_thread = Thread(target=lambda: self.load_api(mpg))
        self.api_thread.start()

        # creates widgets for mpg
        mpg_container = CTkFrame(container)
        mpg_label = CTkLabel(mpg_container, text="Miles Per Gallon:", font=("Arial", 20))
        mpg_label.pack(side="left", padx=10, pady=5)
        spacer = TSCTkButton(mpg_container, text="", fg_color="transparent", width=70, hover=False)
        spacer.pack(side="right", padx=10, pady=5)
        mpg_label = CTkLabel(mpg_container, textvariable=mpg, font=("Arial", 20))
        mpg_label.pack(side="right", pady=5)
        mpg_container.pack(fill="x", padx=10, expand=True)

        # creates mile tracker variables and binds them to a mile manager
        oil_change = DoubleVar(self)
        filter_change = DoubleVar(self)
        oil_change_manager = MileManger("change_oil_at", lambda o: self.after(0, lambda: oil_change.set(o)))
        filter_change_manager = MileManger("change_filter_at", lambda f: self.after(0, lambda: filter_change.set(f)))

        # creates time based maintenance and binds them to date manager
        registration = StringVar(self)
        inspection = StringVar(self)
        registration_manager = DateManager("registration", lambda r: registration.set(r))
        inspection_manager = DateManager("inspection", lambda r: inspection.set(r))

        # creates widgets for oil change
        oil_change_container = CTkFrame(container)
        oil_change_label = CTkLabel(oil_change_container, text="Miles Until Oil Change:", font=("Arial", 20))
        oil_change_label.pack(side="left", padx=10, pady=5)
        oil_change_button = PWCTkButton(oil_change_container, self, 2, text="Reset", font=("Arial", 20), width=70, command=oil_change_manager.reset)
        oil_change_button.pack(side="right", padx=10, pady=5)
        oil_change_label = CTkLabel(oil_change_container, textvariable=oil_change, font=("Arial", 20))
        oil_change_label.pack(side="right", pady=5)
        oil_change_container.pack(fill="x", padx=10, expand=True)

        # creates widgets for filter change
        filter_change_container = CTkFrame(container)
        filter_change_label = CTkLabel(filter_change_container, text="Miles Until Air Filter Change:", font=("Arial", 20))
        filter_change_label.pack(side="left", padx=10, pady=5)
        filter_change_button = PWCTkButton(filter_change_container, self, 2, text="Reset", font=("Arial", 20), width=70, command=filter_change_manager.reset)
        filter_change_button.pack(side="right", padx=10, pady=5)
        filter_change_label = CTkLabel(filter_change_container, textvariable=filter_change, font=("Arial", 20))
        filter_change_label.pack(side="right", pady=5)
        filter_change_container.pack(fill="x", padx=10, expand=True)

        # creates widgets for registration
        registration_calendar = Calendar(self, lambda d: [setattr(registration_manager, "value", d), registration_calendar.place_forget()])
        registration_container = CTkFrame(container)
        registration_label = CTkLabel(registration_container, text="Renew Registration At:", font=("Arial", 20))
        registration_label.pack(side="left", padx=10, pady=5)
        registration_button = PWCTkButton(registration_container, self, 2, text="Reset", font=("Arial", 20), width=70, command=lambda: registration_calendar.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center"))
        registration_button.pack(side="right", padx=10, pady=5)
        registration_label = CTkLabel(registration_container, textvariable=registration, font=("Arial", 20))
        registration_label.pack(side="right", pady=5)
        registration_container.pack(fill="x", padx=10, expand=True)

        # creates widgets for inspection
        inspection_calendar = Calendar(self, lambda d: [setattr(inspection_manager, "value", d), inspection_calendar.place_forget()])
        inspection_container = CTkFrame(container)
        inspection_label = CTkLabel(inspection_container, text="Inspection Due At:", font=("Arial", 20))
        inspection_label.pack(side="left", padx=10, pady=5)
        inspection_button = PWCTkButton(inspection_container, self, 2, text="Reset", font=("Arial", 20), width=70, command=lambda: inspection_calendar.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center"))
        inspection_button.pack(side="right", padx=10, pady=5)
        inspection_label = CTkLabel(inspection_container, textvariable=inspection, font=("Arial", 20))
        inspection_label.pack(side="right", pady=5)
        inspection_container.pack(fill="x", padx=10, expand=True)

        # creates the error codes popup
        self.codes_popup = CTkFrame(self, border_width=2)
        code = CTkLabel(self.codes_popup, text="Code:", font=("Arial", 20))
        description = CTkLabel(self.codes_popup, text="Description:", font=("Arial", 20))
        close_codes = TSCTkButton(self.codes_popup, text="x", width=12, font=("Arial", 20), command=self.codes_popup.place_forget)
        self.codes_container = CTkScrollableFrame(self.codes_popup)
        clear_codes = PWCTkButton(self.codes_popup, self, 2, text="Clear Codes", font=("Arial", 20), command=self.clear_codes)

        # places codes widgets
        close_codes.grid(row=0, column=2, pady=5, padx=5)
        code.grid(row=0, column=0, sticky="s", padx=15)
        description.grid(row=0, column=1, sticky="sw")
        self.codes_container.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=2, pady=(0, 2))
        clear_codes.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 3), padx=3)

        # configures grid for the codes popup
        self.codes_popup.rowconfigure(1, weight=1)
        self.codes_popup.columnconfigure(1, weight=1)
        self.codes_container.columnconfigure(1, weight=1)

    def load_api(self, mpg):
        """
        loads the OBD scanner asynchronously for UI performance
        """

        from Connections.OBDAPI import OBDAPI
        self.api = OBDAPI(
            self,
            self.job_manager,
            lambda m: self.after(0, lambda: mpg.set(m))
        )

    def get_codes(self):
        """
        gets the diagnostic trouble codes (DTCs) from the OBD-II interface and displays them in the UI
        """

        # places popup and clears old codes
        self.api_thread.join()
        self.codes_popup.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center")
        set_widget_scaling(self.appearance_manager.scaling)
        for widget in self.codes_container.winfo_children():
            widget.destroy()

        # gets the new codes and populates the container
        wraplength = 560 * (1 / self.appearance_manager.scaling)
        for row, (code, description) in enumerate(self.api.get_codes()):
            code = CTkLabel(self.codes_container, text=code, font=("Arial", 10))
            description = CTkLabel(self.codes_container, text=description, font=("Arial", 10), wraplength=wraplength, justify="left")
            code.grid(row=row, column=0, padx=10)
            description.grid(row=row, column=1, sticky="w", padx=(25, 0))

    def clear_codes(self):
        """
        clears the diagnostic trouble codes (DTCs) from the OBD-II interface
        """

        self.api.clear_codes()
        self.get_codes()

    def destroy(self):
        """
        overrides the destroy method to also shut down the OBD connection
        """

        self.api_thread.join()
        self.api.shutdown()
        super().destroy()
