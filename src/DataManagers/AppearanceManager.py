from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling, ThemeManager
from json import dump, load
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime


class AppearanceManager:

    # ====================================== ALL VALUES ======================================
    """
    contains the cycle values for the appearance settings.
    Each value has a "next" key that points to the next value in the cycle,
    and an "icon" key that points to the icon to be displayed for that value.
    """
    
    MODES = {
        "light": {"next": "dark", "icon": "🔆"},
        "dark": {"next": "system", "icon": "🌙"},
        "system": {"next": "light", "icon": "🕒"}
    }

    THEMES = {
        "blue": {"next": "green", "icon": "💧"},
        "green": {"next": "dark-blue", "icon": "🍃"},
        "dark-blue": {"next": "blue", "icon": "🌊"}
    }

    SCALES = {
        1.000: {"next": 1.375, "icon": "👁️"},
        1.375: {"next": 1.750, "icon": "🔍"},
        1.750: {"next": 1.000, "icon": "🔭"}
    }

    # ======================================= LOAD/SAVE ======================================

    def __init__(self, root):
        """
        initializes the AppearanceManager with default values and attempts to load the appearance settings from a file.

        @param root: the root widget of the application, used to apply themes and modes
            additionally the root widget is used to schedule the system mode update
        """

        self.mode = "system"
        self.theme = "blue"
        self.scaling = 1.375
        self.lat = 0
        self.long = 0
        self.root = root
        self.after_change_mode = root.after(0, lambda: None)
        self.load()

    def load(self):
        """
        attempts to load the appearance settings from a JSON file.
        If the file does not exist, it creates a new file with default values.
        """

        # attempts to load the appearance settings from a JSON file
        try:
            with open("AppData/appearance_settings.json", "r") as f:
                data = load(f)
                self.mode = data["mode"]
                self.theme = data["theme"]
                self.scaling = data["scaling"]
                self.lat = data["lat"]
                self.long = data["long"]

        # If the file does not exist or is corrupted, create it with default values
        except:
            self.save()

        # updates the appearance settings based on the loaded values
        set_default_color_theme(self.theme)
        set_widget_scaling(self.scaling)
        set_appearance_mode(self.mode) if (self.mode != "system") else self.apply_system_mode()

    def save(self):
        """
        saves the current appearance settings to a JSON file.
        """
        
        with open("AppData/appearance_settings.json", "w") as f:
            dump({
                "mode": self.mode,
                "theme": self.theme,
                "scaling": self.scaling,
                "lat": self.lat,
                "long": self.long
            }, f, indent=4)

    # ======================================= CYCLERS ========================================

    def cycle_mode(self):
        """
        cycles through the appearance modes and applies the selected mode.

        @return: the icon representing the current mode
        """
        
        self.mode = self.MODES[self.mode]["next"]
        self.root.after_cancel(self.after_change_mode)
        set_appearance_mode(self.mode) if (self.mode != "system") else self.apply_system_mode()
        self.save()
        return self.MODES[self.mode]["icon"]

    def cycle_theme(self):
        """
        cycles through the appearance themes and applies the selected theme.

        @return: the icon representing the current theme
        """

        self.theme = self.THEMES[self.theme]["next"]
        set_default_color_theme(self.theme)
        self.change_theme(self.root) if self.root else None
        self.save()
        return self.THEMES[self.theme]["icon"]

    def cycle_scaling(self):
        """
        cycles through the scaling options and applies the selected scale.

        @return: the icon representing the current scale
        """

        self.scaling = self.SCALES[self.scaling]["next"]
        set_widget_scaling(self.scaling)
        self.save()
        return self.SCALES[self.scaling]["icon"]

    # ======================================= HELPERS ========================================

    def apply_system_mode(self):
        """
        Applies the system appearance mode to the application.
        """

        # gets the sunrise and sunset times for the current location
        city = LocationInfo(latitude=self.lat, longitude=self.long) # get gps coords here
        now = datetime.now().astimezone()
        s = sun(city.observer, date=now.date(), tzinfo=now.tzinfo)
        sunrise = s["sunrise"]
        sunset = s["sunset"]

        # sets the mode based on the current time and schedules the next update in 5 minutes
        # self.save() do this when we get gps coords
        set_appearance_mode("light" if sunrise < now < sunset else "dark")
        self.after_change_mode = self.root.after(300_000, self.apply_system_mode)

    def change_theme(self, root):
        """
        Changes the theme of the application.

        @param root: the root widget to apply the theme to
        """

        # finds the widget type and its respective theme in the ThemeManager
        for superclass in type(root).mro():
            if superclass.__name__ in ThemeManager.theme and root.cget("fg_color") != "transparent":
                for key, value in ThemeManager.theme[superclass.__name__].items():

                    # only applies the theme if the key is a valid configuration option for the widget
                    try:
                        root.configure(**{key: value}) if key != "corner_radius" and key != "border_width" else None
                    except ValueError:
                        continue
                break

        # recursively applies the theme to all child widgets
        for widget in root.winfo_children():
            self.change_theme(widget)
