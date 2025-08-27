from Connections.GPIOAPI import GPIOAPI
from Connections.ReleaseAPI import ReleaseAPI
from customtkinter import CTk, StringVar, set_widget_scaling
from DataManagers.AppearanceManager import AppearanceManager
from AppData import PI_WIDTH, PI_HEIGHT
from evdev import list_devices, InputDevice
from os import environ
from UI.MainMenu import MainMenu
from UI.SettingsMenu import SettingsMenu
from UI.MusicMenu import MusicMenu
from UI.MapsMenu import MapsMenu
from UI.OBDMenu import OBDMenu
from threading import Lock
from subprocess import run


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
        self.configure(cursor="none")
        self.geometry(f"{PI_WIDTH}x{PI_HEIGHT}+0+0")
        self.appearance_manager = AppearanceManager(self)
        self.shutdown_lock = Lock()
        GPIOAPI(lambda: self.after(0, self.destroy), self.appearance_manager.apply_system_mode, self.shutdown_lock)
        self.active_menu = "main"
        release_api = ReleaseAPI(lambda: self.destroy)
        temp = StringVar(self, " °F")
        notification = StringVar(self, "Software Update Available in Settings" if release_api.update_available() else "")

        # gets the touch screen device
        device_name = environ["TOUCH_SCREEN"]
        touch_screen = None
        for path in list_devices():
            touch_screen = InputDevice(path)
            if device_name == touch_screen.name:
                break

        # creates the various menus
        self.menus = {
            "main": MainMenu(self, temp, touch_screen, notification),
            "maps": MapsMenu(self),
            "music": MusicMenu(self),
            "obd": OBDMenu(self, temp, self.appearance_manager),
            "settings": SettingsMenu(self, self.appearance_manager, release_api)
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

    def mainloop(self):
        """
        overrides the mainloop to prevent program exit before shutdown command
        is finished executing
        """

        super().mainloop()
        with self.shutdown_lock:
            return
        
    def destroy(self):
        """
        overrides the destroy method to also ensure the backend is stopped before shutdown
        """

        run(["../stop_backend.sh"])
        return super().destroy()
