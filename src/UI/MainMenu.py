from customtkinter import CTkFrame, CTkLabel, CTkButton, StringVar
from Dev.CTkButtonFixed import CTkButtonFixed
from subprocess import run
from evdev import list_devices, InputDevice, ecodes
from os import environ
from datetime import datetime


class MainMenu(CTkFrame):
    """
    the class to represent the main menu of the dashboard
    """

    def __init__(self, master, temp, **kwargs):
        """
        Initializes the main menu frame

        @param master: the parent widget
        @param temp: a StringVar to hold the temperature
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)

        # creates the labels for the buttons
        maps_label = CTkLabel(self, text="Maps", font=("Arial", 20))
        music_label = CTkLabel(self, text="Music", font=("Arial", 20))
        obd_label = CTkLabel(self, text="OBD Scan", font=("Arial", 20))
        settings_label = CTkLabel(self, text="Settings", font=("Arial", 20))
        maps_label.grid(row=0, column=1, sticky="s")
        music_label.grid(row=0, column=3, sticky="s")
        obd_label.grid(row=0, column=5, sticky="s")
        settings_label.grid(row=0, column=7, sticky="s")

        # creates the buttons of the menu
        maps_button = CTkButtonFixed(self, text="🧭", font=("Arial", 100), command=lambda: master.change_menu("maps"))
        music_button = CTkButtonFixed(self, text="🎧", font=("Arial", 100), command=lambda: master.change_menu("music"))
        obd_button = CTkButtonFixed(self, text="🚙", font=("Arial", 100), command=lambda: master.change_menu("obd"))
        settings_button = CTkButtonFixed(self, text="🛠️", font=("Arial", 100), command=lambda: master.change_menu("settings"))
        sleep_button = CTkButton(self, text="Display Sleep", font=("Arial", 20), command=self.sleep)
        maps_button.grid(row=1, column=1)
        music_button.grid(row=1, column=3)
        obd_button.grid(row=1, column=5)
        settings_button.grid(row=1, column=7)
        sleep_button.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")

        # places time label
        self.time = StringVar(self)
        time_label = CTkLabel(self, textvariable=self.time, font=("Arial", 20))
        time_label.grid(row=2, column=1)
        self.update_time()

        # places temperature label
        temp_label = CTkLabel(self, textvariable=temp, font=("Arial", 20))
        temp_label.grid(row=2, column=7)

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

    def update_time(self):
        """
        updates the time display label and queues the next update just after the minute change
        """

        now = datetime.now()
        self.time.set(now.strftime("%I:%M %p"))
        self.after((60 - now.second) * 1000, self.update_time)

    def sleep(self):
        """
        Puts the display to sleep by hiding the main window and turning off the HDMI output.
        It waits for a touch event to wake up the display, then re-enables the HDMI
        output and shows the main window again.
        """

        # Hide the main window and turn off the HDMI output
        self.winfo_toplevel().withdraw()
        run(["xrandr", "--output", "HDMI-1", "--off", "--output", "HDMI-2", "--off"])

        # gets the touch screen device
        device_name = environ["TOUCH_SCREEN"]
        touch_screen = None
        for path in list_devices():
            touch_screen = InputDevice(path)
            if device_name == touch_screen.name:
                break

        # Wait for a touch event to wake up the display
        for event in touch_screen.read_loop():
            if event.code == ecodes.BTN_TOUCH and event.value == 1:
                break
        
        # Re-enable the HDMI output and show the main window again
        run(["xrandr", "--output", "HDMI-1", "--auto", "--output", "HDMI-2", "--auto"])
        self.winfo_toplevel().deiconify()
