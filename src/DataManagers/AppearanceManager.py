from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling, ThemeManager
from json import dump, load
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime


class AppearanceManager:

    # ==================================== DEFAULT VALUES ====================================

    root = None  # the will be set by the MenuManager when it is created
    after_change_mode = None  # used to change the mode on sunrise/sunset if the mode is set to "system"
    mode = "system"
    theme = "blue"
    scaling = 1.375
    lat = 0
    long = 0

    # ====================================== ALL VALUES ======================================

    # class to hold metadata for each value used by the UI to cycle through options and display the current value
    class MetaData:
        def __init__(self, next_value, icon):
            self.NEXT = next_value
            self.ICON = icon

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

    # ======================================= SETTERS ========================================

    @classmethod
    def cycle_mode(cls):
        cls.mode = cls.MODES[cls.mode].NEXT
        cls.root.after_cancel(cls.after_change_mode)
        set_appearance_mode(cls.mode) if (cls.mode != "system") else cls.apply_system_mode()
        cls.save()
        return cls.MODES[cls.mode].ICON
        
    @classmethod
    def cycle_theme(cls):
        cls.theme = cls.THEMES[cls.theme].NEXT
        set_default_color_theme(cls.theme)
        cls.change_theme(cls.root) if cls.root else None
        cls.save()
        return cls.THEMES[cls.theme].ICON

    @classmethod
    def cycle_scaling(cls):
        cls.scaling = cls.SCALES[cls.scaling].NEXT
        set_widget_scaling(cls.scaling)
        cls.save()
        return cls.SCALES[cls.scaling].ICON

    # ======================================= LOAD/SAVE ======================================

    @classmethod
    def load(cls):
        try:
            with open("AppData/appearance_settings.json", "r") as f:
                data = load(f)
                cls.mode = data["mode"]
                cls.theme = data["theme"]
                cls.scaling = data["scaling"]
                cls.lat = data["lat"]
                cls.long = data["long"]
        
        # If the file does not exist, create it with default values
        except FileNotFoundError:
            cls.save()

        set_default_color_theme(cls.theme)
        set_widget_scaling(cls.scaling)

    @classmethod
    def set_root(cls, root):
        cls.root = root
        cls.after_change_mode = root.after(0, lambda: None)
        set_appearance_mode(cls.mode) if (cls.mode != "system") else cls.apply_system_mode()

    @classmethod
    def save(cls):
        with open("AppData/appearance_settings.json", "w") as f:
            dump({
                "mode": cls.mode,
                "theme": cls.theme,
                "scaling": cls.scaling,
                "lat": cls.lat,
                "long": cls.long
            }, f, indent=4)

    # ======================================= HELPERS ========================================

    @classmethod
    def apply_system_mode(cls):
        """
        Applies the system appearance mode to the application.
        """

        # gets the sunrise and sunset times for the current location
        # location = ip("me")
        # cls.lat, cls.long = location.latlng if location.latlng else (cls.lat, cls.long)
        city = LocationInfo(latitude=cls.lat, longitude=cls.long)
        now = datetime.now().astimezone()
        s = sun(city.observer, date=now.date(), tzinfo=now.tzinfo)
        sunrise = s["sunrise"]
        sunset = s["sunset"]

        # sets the mode based on the current time and schedules the next update in 30 minutes
        cls.save()
        set_appearance_mode("light" if sunrise < now < sunset else "dark")
        cls.after_change_mode = cls.root.after(1_800_000, cls.apply_system_mode)

    @classmethod
    def change_theme(cls, root):
        """
        Changes the theme of the application.
        
        @param root: the root widget to apply the theme to
        """

        # finds the widget type and its respective theme in the ThemeManager
        for superclass in type(root).mro():
            if superclass.__name__ in ThemeManager.theme:
                for key, value in ThemeManager.theme[superclass.__name__].items():

                    # only applies the theme if the key is a valid configuration option for the widget
                    try:
                        root.configure(**{key: value}) if root.cget("fg_color") != "transparent" else None
                    except ValueError:
                        continue
                break

        # recursively applies the theme to all child widgets
        for widget in root.winfo_children():
            cls.change_theme(widget)
