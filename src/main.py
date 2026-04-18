from UI.MenuManager import MenuManager
from Dev.KeyboardController import KeyboardController


if __name__ == "__main__":
    print("Starting Debug Logging")
    window = MenuManager()
    KeyboardController(window)
    return_code = window.mainloop()
    print("Ending Debug Logging")
    exit(return_code)
