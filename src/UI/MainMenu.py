from customtkinter import CTkFrame, CTkLabel, CTkButton
from AppData import ICON_FONT, LABEL_FONT
from subprocess import run


class MainMenu(CTkFrame):
    """
    the class to represent the main menu of the dashboard
    """

    def __init__(self, parent, fg_color=None, **kwargs):
        """
        Initializes the main menu frame

        @param parent: the parent widget
        @param fg_color: the foreground color of the frame
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(parent, fg_color=fg_color, **kwargs)

        # creates the labels for the buttons
        maps_label = CTkLabel(self, text="Maps", font=LABEL_FONT)
        music_label = CTkLabel(self, text="Music", font=LABEL_FONT)
        obd_label = CTkLabel(self, text="OBD Scan", font=LABEL_FONT)
        settings_label = CTkLabel(self, text="Settings", font=LABEL_FONT)
        maps_label.grid(row=0, column=1, sticky="s")
        music_label.grid(row=0, column=3, sticky="s")
        obd_label.grid(row=0, column=5, sticky="s")
        settings_label.grid(row=0, column=7, sticky="s")

        # creates the buttons of the menu
        maps_button = CTkButton(self, text="🧭", font=ICON_FONT, command=lambda: parent.change_menu("maps"))
        music_button = CTkButton(self, text="🎧", font=ICON_FONT, command=lambda: parent.change_menu("music"))
        obd_button = CTkButton(self, text="🚙", font=ICON_FONT, command=lambda: parent.change_menu("obd"))
        settings_button = CTkButton(self, text="🛠️", font=ICON_FONT, command=lambda: parent.change_menu("settings"))
        sleep_button = CTkButton(self, text="Display Off", font=LABEL_FONT, command=lambda: run(["xrandr", "--output", "HDMI-1", "--off"]))
        maps_button.grid(row=1, column=1, sticky="nsew")
        music_button.grid(row=1, column=3, sticky="nsew")
        obd_button.grid(row=1, column=5, sticky="nsew")
        settings_button.grid(row=1, column=7, sticky="nsew")
        sleep_button.grid(row=2, column=1, columnspan=7, pady=(0, 10), sticky="sew")

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)
        