from customtkinter import CTk, set_widget_scaling
from DataManagers.AppearanceManager import AppearanceManager
from AppData import PI_WIDTH, PI_HEIGHT
from UI.MainMenu import MainMenu
from UI.SettingsMenu import SettingsMenu
from UI.MusicMenu import MusicMenu
from UI.MapsMenu import MapsMenu
from UI.OBDMenu import OBDMenu


class MenuManager(CTk):
    """
    the class to represent the screen that manages the various menus in the application
    """

    def __init__(self, **kwargs):
        """
        Initializes the window and loads the main menu

        @param kwargs: additional keyword arguments for CTk
        """

        # initializes the window
        super().__init__(**kwargs)
        self.appearance_manager = AppearanceManager(self)
        self.geometry(f"{PI_WIDTH}x{PI_HEIGHT}+0+0")
        self.active_menu = "main"

        # creates the various menus
        self.menus = {
            "main": MainMenu(self),
            "maps": MapsMenu(self),
            "music": MusicMenu(self),
            "obd": OBDMenu(self),
            "settings": SettingsMenu(self, self.appearance_manager)
        }
        self.change_menu(self.active_menu)

    def change_menu(self, menu_name):
        """
        Changes the active menu to the specified menu name

        @param menu_name: the name of the menu to switch to
        """
        
        self.menus[self.active_menu].place_forget()
        self.active_menu = menu_name
        self.menus[self.active_menu].place(relx=0, rely=0, relwidth=1, relheight=1)
        set_widget_scaling(self.appearance_manager.scaling)
