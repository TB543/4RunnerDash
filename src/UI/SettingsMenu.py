from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, set_widget_scaling
from Dev.TSCTkButton import TSCTkButton
from Dev.CTkButtonFixed import CTkButtonFixed
from Dev.PWCTkButton import PWCTkButton
from DataManagers.AppearanceManager import AppearanceManager
from AppData import APPS


class SettingsMenu(CTkFrame):
    """
    Settings menu for the 4Runner Dash application.
    """

    def __init__(self, master, appearance_manager, fg_job_manager, release_api, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param appearance_manager: a reference to the apps appearance manager
        @param fg_job_manager: a reference to the fg job manager
        @param release_api: a reference to the apps release api
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.appearance_manager = appearance_manager
        self.fg_job_manager = fg_job_manager
        appearance_text = AppearanceManager.MODES[self.appearance_manager.mode]["icon"]
        theme_text = AppearanceManager.THEMES[self.appearance_manager.theme]["icon"]
        scale_text = AppearanceManager.SCALES[self.appearance_manager.scaling]["icon"]

        # creates the labels for the buttons
        appearance_label = CTkLabel(self, text="Appearance", font=("Arial", 20))
        theme_label = CTkLabel(self, text="Theme", font=("Arial", 20))
        scale_label = CTkLabel(self, text="Zoom", font=("Arial", 20))
        apps_label = CTkLabel(self, text="Apps", font=("Arial", 20))
        appearance_label.grid(row=0, column=1, sticky="s")
        theme_label.grid(row=0, column=3, sticky="s")
        scale_label.grid(row=0, column=5, sticky="s")
        apps_label.grid(row=0, column=7, sticky="s")

        # creates the buttons of the menu
        appearance_button = CTkButtonFixed(self, text=appearance_text, font=("Arial", 100), command=lambda: appearance_button.configure(text=self.appearance_manager.cycle_mode()))
        theme_button = CTkButtonFixed(self, text=theme_text, font=("Arial", 100), command=lambda: theme_button.configure(text=self.appearance_manager.cycle_theme()))
        scale_button = CTkButtonFixed(self, text=scale_text, font=("Arial", 100), command=lambda: scale_button.configure(text=self.appearance_manager.cycle_scaling()))
        apps_button = CTkButtonFixed(self, text="📱", font=("Arial", 100), command=self.show_apps_menu)
        back_button = TSCTkButton(self, text="Main Menu", font=("Arial", 20), command=lambda: master.change_menu("main"))
        update_button = PWCTkButton(self, self, text="Update Software", font=("Arial", 20), command=release_api.update)
        appearance_button.grid(row=1, column=1)
        theme_button.grid(row=1, column=3)
        scale_button.grid(row=1, column=5)
        apps_button.grid(row=1, column=7)
        back_button.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        release_api.add_callback(lambda: self.after(0, lambda: update_button.grid(row=2, column=1, columnspan=7, pady=(0, 10), sticky="sew")))

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

        # creates apps menu
        self.apps_menu = CTkFrame(self, border_width=2)
        apps_menu_label = CTkLabel(self.apps_menu, text="Select an external app to open:", font=("Arial", 20))
        close_apps_menu = TSCTkButton(self.apps_menu, text="x", width=12, font=("Arial", 20),command=self.apps_menu.place_forget)
        apps_container = CTkScrollableFrame(self.apps_menu)
        apps_menu_label.grid(row=0, column=0)
        close_apps_menu.grid(row=0, column=1, pady=5, padx=5)
        apps_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=(0, 2))
        self.apps_menu.rowconfigure(1, weight=1)
        self.apps_menu.columnconfigure(0, weight=1)

        # adds apps to apps menu
        for name, config in APPS.items():
            if config:
                app = TSCTkButton(apps_container, text=name, font=("Arial", 20), command=lambda c=config: self.start_app(c))
                app.pack(fill="x", expand=True, padx=5, pady=5)

            # shell command will be password protected
            else:
                app = PWCTkButton(apps_container, self, text=name, font=("Arial", 20), command=lambda c=config: self.start_app(c))
                app.pack(fill="x", expand=True, padx=5, pady=5)

    def show_apps_menu(self):
        """
        displays the menu of all the additional applications that can be run
        """

        self.apps_menu.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center")
        set_widget_scaling(self.appearance_manager.scaling)

    def start_app(self, config):
        """
        starts an app
        this program will be hidden but continue running in the background until app has exited

        @param config: the config that will be executed to start the app
        """

        # no config - default command for opening shell
        if config is None:
            self.winfo_toplevel().destroy()

        # hides this program and opens the app
        else:
            self.winfo_toplevel().withdraw()
            self.fg_job_manager.start_application(lambda: self.winfo_toplevel().deiconify(), **config)
