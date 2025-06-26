from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling
from json import dump, load

class APPEARANCE_SETTINGS:

    # ==================================== DEFAULT VALUES ====================================

    _mode = "light"
    _theme = "dark-blue"
    _scaling = 2.0

    # ======================================= SETTERS ========================================

    @classmethod
    def set_mode(cls, mode):
        set_appearance_mode(mode)
        cls._mode = mode

    @classmethod
    def set_theme(cls, theme):
        set_default_color_theme(theme)
        cls._theme = theme

    @classmethod
    def set_scaling(cls, scaling):
        set_widget_scaling(scaling)
        cls._scaling = scaling

    # ======================================= LOAD/SAVE ======================================

    @classmethod
    def load(cls):
        try:
            with open("AppData/json/appearance_settings.json", "r") as f:
                data = load(f)
                cls.set_mode(data["mode"])
                cls.set_theme(data["theme"])
                cls.set_scaling(data["scaling"])
        
        # If the file does not exist, create it with default values
        except FileNotFoundError:
            cls.save()
            cls.load()

    @classmethod
    def save(cls):
        with open("AppData/json/appearance_settings.json", "w") as f:
            dump({
                "mode": cls._mode,
                "theme": cls._theme,
                "scaling": cls._scaling
            }, f, indent=4)
