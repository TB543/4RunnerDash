from UI import *
from Dev import KeyboardController


window = MenuManager()
KeyboardController.set_handler(window)
window.mainloop()
