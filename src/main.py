from UI.MenuManager import MenuManager
from Dev.KeyboardController import KeyboardController


if __name__ == "__main__":
    window = MenuManager()
    KeyboardController(window)
    return_code = window.mainloop()
    exit(return_code)
