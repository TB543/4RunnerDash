from threading import Thread
from Music import start_bluetooth
from UI import *
from Dev import KeyboardController


if __name__ == "__main__":
    Thread(target=start_bluetooth, daemon=True).start()
    window = MenuManager()
    KeyboardController(window)
    window.mainloop()
