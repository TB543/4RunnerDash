from UI.MenuManager import MenuManager
from threading import Thread
from subprocess import run
from Dev.KeyboardController import KeyboardController


if __name__ == "__main__":
    window = MenuManager()
    KeyboardController(window)
    return_code = window.mainloop()
    exit(return_code)
