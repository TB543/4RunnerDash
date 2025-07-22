from customtkinter import CTkFrame, CTkLabel, CTkButton
from Dev.CTkButtonFixed import CTkButtonFixed
from DataManagers.AppearanceManager import AppearanceManager
from subprocess import run


class SettingsMenu(CTkFrame):
    """
    Settings menu for the 4Runner Dash application.
    """

    def __init__(self, master, appearance_manager, **kwargs):
        """
        Initializes the settings menu frame.
        
        @param master: the parent widget
        @param appearance_manager: a reference to the apps appearance manager
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        appearance_text = AppearanceManager.MODES[appearance_manager.mode]["icon"]
        theme_text = AppearanceManager.THEMES[appearance_manager.theme]["icon"]
        scale_text = AppearanceManager.SCALES[appearance_manager.scaling]["icon"]

        # creates the labels for the buttons
        appearance_label = CTkLabel(self, text="Appearance", font=("Arial", 20))
        theme_label = CTkLabel(self, text="Theme", font=("Arial", 20))
        scale_label = CTkLabel(self, text="Zoom", font=("Arial", 20))
        shell_label = CTkLabel(self, text="Open Shell", font=("Arial", 20))
        appearance_label.grid(row=0, column=1, sticky="s")
        theme_label.grid(row=0, column=3, sticky="s")
        scale_label.grid(row=0, column=5, sticky="s")
        shell_label.grid(row=0, column=7, sticky="s")

        # creates the buttons of the menu
        appearance_button = CTkButtonFixed(self, text=appearance_text, font=("Arial", 100), command=lambda: appearance_button.configure(text=appearance_manager.cycle_mode()))
        theme_button = CTkButtonFixed(self, text=theme_text, font=("Arial", 100), command=lambda: theme_button.configure(text=appearance_manager.cycle_theme()))
        scale_button = CTkButtonFixed(self, text=scale_text, font=("Arial", 100), command=lambda: scale_button.configure(text=appearance_manager.cycle_scaling()))
        shell_button = CTkButtonFixed(self, text="🖥️", font=("Arial", 100), command=self.open_shell)
        back_button = CTkButton(self, text="Main Menu", font=("Arial", 20), command=lambda: master.change_menu("main"))
        appearance_button.grid(row=1, column=1)
        theme_button.grid(row=1, column=3)
        scale_button.grid(row=1, column=5)
        shell_button.grid(row=1, column=7)
        back_button.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

    def open_shell(self):
        """
        kills the display and opens the terminal shell.
        """
        
        self.winfo_toplevel().destroy()
        run(["sudo", "killall", "Xorg"])
