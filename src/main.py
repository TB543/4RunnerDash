from UI.MenuManager import MenuManager
from threading import Thread
from Dev.KeyboardController import KeyboardController
try:
    from Lib.BluezAgent import my_app as start_bluetooth
except ModuleNotFoundError:
    from Dev.Imports.BluezAgent import *


if __name__ == "__main__":
    Thread(target=start_bluetooth, daemon=True).start()
    window = MenuManager()
    KeyboardController(window)
    window.mainloop()
