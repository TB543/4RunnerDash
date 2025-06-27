from customtkinter import set_appearance_mode, set_default_color_theme, set_widget_scaling, ThemeManager
from json import dump, load


def change_theme(root):
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
                    root.configure(**{key: value})
                except ValueError:
                    continue
            break

    # recursively applies the theme to all child widgets
    for widget in root.winfo_children():
        change_theme(widget)


class APPEARANCE_SETTINGS:

    # ==================================== DEFAULT VALUES ====================================

    mode = "dark"
    theme = "blue"
    scaling = 1.00

    # ====================================== ALL VALUES ======================================

    # class to hold metadata for each value used by the UI to cycle through options and display the current value
    class MetaData:
        def __init__(self, next, icon):
            self.NEXT = next
            self.ICON = icon

    MODES = {
        "light": MetaData("dark", "☀️"),
        "dark": MetaData("light", "🌙"),
        "system": MetaData("light", "🕒")  # todo implement system to switch based based on time of day
    }

    THEMES = {
        "blue": MetaData("green", "💧"),
        "green": MetaData("dark-blue", "🍃"),
        "dark-blue": MetaData("blue", "🌊"),
    }

    SCALES = {
        1.00: MetaData(1.37, "👁️"),
        1.37: MetaData(1.75, "🔍"),
        1.75: MetaData(1.00, "🔭")
    }

    # ======================================= SETTERS ========================================

    @classmethod
    def set_mode(cls, mode):
        set_appearance_mode(mode)
        cls.mode = mode

    @classmethod
    def set_theme(cls, theme, root=None):
        set_default_color_theme(theme)
        cls.theme = theme
        change_theme(root) if root else None


    @classmethod
    def set_scaling(cls, scaling):
        set_widget_scaling(scaling)
        cls.scaling = scaling

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
                "mode": cls.mode,
                "theme": cls.theme,
                "scaling": cls.scaling
            }, f, indent=4)
