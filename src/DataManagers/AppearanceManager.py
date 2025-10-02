from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling, ThemeManager, CTkFrame
from tkintermapview import TkinterMapView
from json import dump, load
from AppData import PI_WIDTH


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
        PI_WIDTH / 1024: {"next": (PI_WIDTH / 1024) + .375, "icon": "👁️"},
        (PI_WIDTH / 1024) + .375: {"next": (PI_WIDTH / 1024) + .75, "icon": "🔍"},
        (PI_WIDTH / 1024) + .75: {"next": (PI_WIDTH / 1024), "icon": "🔭"}
    }

    # ======================================= LOAD/SAVE ======================================

    def __init__(self, root):
        """
        initializes the AppearanceManager with default values and attempts to load the appearance settings from a file.

        @param root: the root widget of the application, used to apply themes and modes
            additionally the root widget is used to schedule the system mode update
        """

        self.mode = "system"
        self.system_mode = 0  # will be initialized by GPIOAPI
        self.theme = "blue"
        self.scaling = list(AppearanceManager.SCALES.keys())[1]
        self.root = root
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
                AppearanceManager.SCALES[data["scaling"]]  # error if pi resolution settings change and resets data
                self.mode = data["mode"]
                self.theme = data["theme"]
                self.scaling = data["scaling"]
        except:
            pass

        # updates the appearance settings based on the loaded values
        set_default_color_theme(self.theme)
        set_widget_scaling(self.scaling)
        set_appearance_mode(self.mode) if (self.mode != "system") else self.apply_system_mode(self.system_mode)

    def save(self):
        """
        saves the current appearance settings to a JSON file.
        """
        
        with open("AppData/appearance_settings.json", "w") as f:
            dump({
                "mode": self.mode,
                "theme": self.theme,
                "scaling": self.scaling,
            }, f, indent=4)

    # ======================================= CYCLERS ========================================

    def cycle_mode(self):
        """
        cycles through the appearance modes and applies the selected mode.

        @return: the icon representing the current mode
        """
        
        self.mode = self.MODES[self.mode]["next"]
        set_appearance_mode(self.mode) if self.mode != "system" else self.apply_system_mode(self.system_mode)
        self.save()
        return self.MODES[self.mode]["icon"]

    def cycle_theme(self):
        """
        cycles through the appearance themes and applies the selected theme.

        @return: the icon representing the current theme
        """

        old_theme = ThemeManager.theme
        self.theme = self.THEMES[self.theme]["next"]
        set_default_color_theme(self.theme)
        self.change_theme(self.root, old_theme) if self.root else None
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

    def apply_system_mode(self, mode):
        """
        Applies the system appearance mode to the application.

        @param mode: the new system mode: 0 for light, 1 for dark
        """

        self.system_mode = mode
        if self.mode == "system":
            self.root.after(0, lambda: set_appearance_mode("light" if self.system_mode == 0 else "dark"))

    def change_theme(self, root, old_theme):
        """
        Changes the theme of the application.

        @param root: the root widget to apply the theme to
        @param old_top_fg_color: the old theme, used to keep settings not
            auto applied by theme manager
        """

        # finds the widget type and its respective theme in the ThemeManager
        for superclass in type(root).mro():
            if superclass.__name__ in ThemeManager.theme:
                for key, value in ThemeManager.theme[superclass.__name__].items():

                    # only applies the theme if the key is a valid configuration option for the widget
                    try:
                        if superclass == CTkFrame and key == "fg_color" and root.cget("fg_color") == old_theme["CTkFrame"]["top_fg_color"]:
                            value = ThemeManager.theme["CTkFrame"]["top_fg_color"]
                        root.configure(**{key: value}) if root.cget(key) == old_theme[superclass.__name__][key] else None
                    except ValueError:
                        continue
                break

            # ensures map theme changes
            if superclass == TkinterMapView:
                root.bg_color = root.master._apply_appearance_mode(root.master.cget("fg_color"))
                root.draw_rounded_corners()
                break

        # recursively applies the theme to all child widgets
        for widget in root.winfo_children():
            self.change_theme(widget, old_theme)
