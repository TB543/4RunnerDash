from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling, ThemeManager
from json import dump, load
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime


class AppearanceManager:

    # ====================================== ALL VALUES ======================================

    # class to hold metadata for each value used by the UI to cycle through options and display the current value
    class MetaData:
        def __init__(self, next_value, icon):
            self.next = next_value
            self.icon = icon

    MODES = {
        "light": MetaData("dark", "🔆"),
        "dark": MetaData("system", "🌙"),
        "system": MetaData("light", "🕒")
    }

    THEMES = {
        "blue": MetaData("green", "💧"),
        "green": MetaData("dark-blue", "🍃"),
        "dark-blue": MetaData("blue", "🌊"),
    }

    SCALES = {
        1.000: MetaData(1.375, "👁️"),
        1.375: MetaData(1.750, "🔍"),
        1.750: MetaData(1.000, "🔭")
    }

    # ======================================= CYCLERS ========================================

    def cycle_mode(self):
        self.mode = self.MODES[self.mode].next
        self.root.after_cancel(self.after_change_mode)
        set_appearance_mode(self.mode) if (self.mode != "system") else self.apply_system_mode()
        self.save()
        return self.MODES[self.mode].icon
        
    def cycle_theme(self):
        self.theme = self.THEMES[self.theme].next
        set_default_color_theme(self.theme)
        self.change_theme(self.root) if self.root else None
        self.save()
        return self.THEMES[self.theme].icon

    def cycle_scaling(self):
        self.scaling = self.SCALES[self.scaling].next
        set_widget_scaling(self.scaling)
        self.save()
        return self.SCALES[self.scaling].icon

    # ======================================= LOAD/SAVE ======================================

    def __init__(self, root):
        self.mode = "system"
        self.theme = "blue"
        self.scaling = 1.375
        self.lat = 0
        self.long = 0
        self.root = root
        self.after_change_mode = root.after(0, lambda: None)
        self.load()

    def load(self):
        try:
            with open("AppData/appearance_settings.json", "r") as f:
                data = load(f)
                self.mode = data["mode"]
                self.theme = data["theme"]
                self.scaling = data["scaling"]
                self.lat = data["lat"]
                self.long = data["long"]
        
        # If the file does not exist, create it with default values
        except FileNotFoundError:
            self.save()

        set_default_color_theme(self.theme)
        set_widget_scaling(self.scaling)
        set_appearance_mode(self.mode) if (self.mode != "system") else self.apply_system_mode()

    def save(self):
        with open("AppData/appearance_settings.json", "w") as f:
            dump({
                "mode": self.mode,
                "theme": self.theme,
                "scaling": self.scaling,
                "lat": self.lat,
                "long": self.long
            }, f, indent=4)

    # ======================================= HELPERS ========================================

    def apply_system_mode(self):
        """
        Applies the system appearance mode to the application.
        """

        # gets the sunrise and sunset times for the current location
        city = LocationInfo(latitude=self.lat, longitude=self.long)
        now = datetime.now().astimezone()
        s = sun(city.observer, date=now.date(), tzinfo=now.tzinfo)
        sunrise = s["sunrise"]
        sunset = s["sunset"]

        # sets the mode based on the current time and schedules the next update in 30 minutes
        self.save()
        set_appearance_mode("light" if sunrise < now < sunset else "dark")
        self.after_change_mode = self.root.after(1_800_000, self.apply_system_mode)

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
                        root.configure(**{key: value}) if key != "corner_radius" else None
                    except ValueError:
                        continue
                break

        # recursively applies the theme to all child widgets
        for widget in root.winfo_children():
            self.change_theme(widget)
