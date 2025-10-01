from Tools.scripts.nm2def import export_list

from Connections.GPIOAPI import GPIOAPI
from Connections.ReleaseAPI import ReleaseAPI
from customtkinter import CTk, CTkProgressBar, CTkFrame, StringVar, set_widget_scaling
from DataManagers.AppearanceManager import AppearanceManager
from AppData import PI_WIDTH, PI_HEIGHT
from os import environ, name
from DataManagers.FGJobManager import FGJobManager
from UI.MainMenu import MainMenu
from UI.SettingsMenu import SettingsMenu
from UI.MusicMenu import MusicMenu
from UI.MapsMenu import MapsMenu
from UI.OBDMenu import OBDMenu
from threading import Lock
from subprocess import run
try:
    from evdev import list_devices, InputDevice
except ModuleNotFoundError:
    from Dev.Imports.evdev import *


class MenuManager(CTk):
    """
    the class to represent the screen that manages the various menus in the application
    """

    def __init__(self, **kwargs):
        """
        Initializes the window and loads the main menu

        @param kwargs: additional keyword arguments for CTk
        """

        # gets the touch screen device
        device_name = environ["TOUCH_SCREEN"]
        touch_screen = None  # created here because will be used by map menu for custom map touch screen zoom later
        for path in list_devices():
            touch_screen = InputDevice(path)
            if device_name == touch_screen.name:
                break

        # initializes the window
        super().__init__(**kwargs)
        self.configure(cursor="none")
        self.geometry(f"{PI_WIDTH}x{PI_HEIGHT}+0+0")
        self.appearance_manager = AppearanceManager(self)
        self.shutdown_lock = Lock()
        self.fg_job_manager = FGJobManager(touch_screen)
        GPIOAPI(lambda: self.after(0, self.destroy), self.appearance_manager.apply_system_mode, lambda v: self.after(0, lambda: self.show_volume(v)), self.shutdown_lock)
        release_api = ReleaseAPI(self.destroy)
        notification = StringVar(self, "Software Update Available in Settings" if release_api.update_available() else "")

        # creates the various menus
        self.menus = {
            "main": MainMenu(self, notification, self.fg_job_manager, self.appearance_manager.scaling),
            "maps": MapsMenu(self),
            "music": MusicMenu(self),
            "obd": OBDMenu(self, self.appearance_manager),
            "settings": SettingsMenu(self, self.appearance_manager, release_api)
        }
        self.active_menu = "main"
        self.change_menu(self.active_menu)

        # creates volume popup
        self.volume_popup = CTkFrame(self, border_width=2, bg_color=self.menus[self.active_menu].cget("fg_color"))
        self.volume_bar = CTkProgressBar(self.volume_popup, orientation="vertical")
        self.volume_bar.pack(fill="both", expand=True, padx=5, pady=5)
        self.volume_after = self.after(0, lambda: None)

    def change_menu(self, menu_name):
        """
        Changes the active menu to the specified menu name

        @param menu_name: the name of the menu to switch to
        """
        
        self.menus[self.active_menu].place_forget()
        self.active_menu = menu_name
        self.menus[self.active_menu].place(relx=0, rely=0, relwidth=1, relheight=1)
        set_widget_scaling(self.appearance_manager.scaling)

    def show_volume(self, value):
        """
        briefly shows the volume level

        @param value: the volume level
        """

        self.after_cancel(self.volume_after)
        self.volume_bar.set(value)
        self.volume_popup.place(relx=.07, rely=.5, relheight=.7, anchor="center")
        self.volume_after = self.after(1000, self.volume_popup.place_forget)

    def mainloop(self):
        """
        overrides the mainloop to prevent program exit before shutdown command
        is finished executing
        """

        print("Starting Debug Logging")
        super().mainloop()
        with self.shutdown_lock:
            return

    def destroy(self):
        """
        overrides the destroy method to also ensure the backend is stopped before shutdown
        """

        self.fg_job_manager.shutdown(cancel_futures=True, wait=False)
        super().destroy()
        print("Ending Debug Logging")
        if name != "nt":
            run(["../stop_backend.sh"])
