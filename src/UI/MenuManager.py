from customtkinter import CTk
from AppData import PI_WIDTH, PI_HEIGHT, APPEARANCE_MANAGER
from UI.MainMenu import MainMenu
from UI.SettingsMenu import SettingsMenu


class MenuManager(CTk):
    """
    the class to represent the screen that manages the various menus in the application
    """

    def __init__(self, fg_color = None, **kwargs):
        """
        Initializes the window and loads the main menu

        @param fg_color: the foreground color of the window
        @param kwargs: additional keyword arguments for CTk
        """

        # initializes the window
        super().__init__(fg_color, **kwargs)
        APPEARANCE_MANAGER.set_root(self)
        self.geometry(f"{PI_WIDTH}x{PI_HEIGHT}+0+0")
        self.active_menu = "main"

        # creates the various menus
        self.menus = {
            "main": MainMenu(self),
            "settings": SettingsMenu(self)
        }
        self.menus[self.active_menu].place(relx=0, rely=0, relwidth=1, relheight=1)

    def change_menu(self, menu_name):
        """
        Changes the active menu to the specified menu name

        @param menu_name: the name of the menu to switch to
        """
        
        self.menus[self.active_menu].place_forget()
        self.active_menu = menu_name
        self.menus[self.active_menu].place(relx=0, rely=0, relwidth=1, relheight=1)
        APPEARANCE_MANAGER.set_scaling(APPEARANCE_MANAGER.scaling)
