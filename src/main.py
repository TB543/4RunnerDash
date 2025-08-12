from UI.MenuManager import MenuManager
from threading import Thread
from Lib.BluezAgent import my_app as start_bluetooth
from Dev.KeyboardController import KeyboardController


if __name__ == "__main__":
    Thread(target=start_bluetooth, daemon=True).start()
    window = MenuManager()
    KeyboardController(window)
    window.mainloop()
