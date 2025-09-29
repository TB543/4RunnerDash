from customtkinter import CTkFrame, CTkLabel, StringVar, CTkScrollableFrame
from Connections.GPIOAPI import GPIOAPI
from Dev.TSCTkButton import TSCTkButton
from Dev.CTkButtonFixed import CTkButtonFixed
from subprocess import run
from datetime import datetime
from os.path import exists
from os import remove


class MainMenu(CTkFrame):
    """
    the class to represent the main menu of the dashboard
    """

    def __init__(self, master, notification, fg_job_manager, scale, **kwargs):
        """
        Initializes the main menu frame

        @param master: the parent widget
        @param notification: a string var to display notifications from the various menus
        @param fg_job_manager: an instance of the foreground job manager for display sleep jobs
        @param scale: the appearance scale, determines the wrap length of the patch notes
        @param kwargs: additional keyword arguments for CTkFrame
        """

        # initialize fields
        super().__init__(master, **kwargs)
        self.fg_job_manager = fg_job_manager

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
        sleep_button = TSCTkButton(self, text="Display Sleep", font=("Arial", 20), command=self.sleep)
        maps_button.grid(row=1, column=1)
        music_button.grid(row=1, column=3)
        obd_button.grid(row=1, column=5)
        settings_button.grid(row=1, column=7)
        sleep_button.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")

        # places time label
        self.time = StringVar(self)
        time_label = CTkLabel(self, textvariable=self.time, font=("Arial", 20))
        time_label.grid(row=2, column=1, sticky="s", pady=20)
        self.update_time()

        # places notification label
        notification_label = CTkLabel(self, textvariable=notification, font=("Arial", 15))
        notification_label.grid(row=2, column=2, columnspan=5, sticky="sew", pady=20)

        # places temperature label
        self.temp = StringVar(self, f" °F")
        temp_label = CTkLabel(self, textvariable=self.temp, font=("Arial", 20))
        temp_label.grid(row=2, column=7, sticky="s", pady=20)
        self.update_temp()

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(2, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)

        # gets patch notes
        if exists("AppData/patch_notes.txt"):
            wraplength = 725 * (1 / scale)
            with open("AppData/patch_notes.txt") as f:
                patch_notes = f.read()

            # creates widgets to display patch notes
            patch_notes_frame = CTkFrame(self, border_width=2)
            header = CTkLabel(patch_notes_frame, text="Patch Notes:", font=("Arial", 20))
            close_patch_notes = TSCTkButton(patch_notes_frame, text="x", width=12, font=("Arial", 20), command=lambda: MainMenu.close_patch_notes(patch_notes_frame))
            patch_notes_container = CTkScrollableFrame(patch_notes_frame)
            patch_notes = CTkLabel(patch_notes_container, text=patch_notes, justify="left", wraplength=wraplength, font=("Arial", 10))

            # places patch notes widgets
            self.after(0, lambda: patch_notes.pack(side="left"))
            header.grid(row=0, column=0, padx=15)
            close_patch_notes.grid(row=0, column=1, pady=5, padx=5)
            patch_notes_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=(0, 2))
            patch_notes_frame.place(relx=.5, rely=.5, relwidth=.75, relheight=.75, anchor="center")
            patch_notes_frame.rowconfigure(1, weight=1)
            patch_notes_frame.columnconfigure(0, weight=1)

    def update_time(self):
        """
        updates the time display label and queues the next update just after the minute change
        """

        now = datetime.now()
        self.time.set(now.strftime("%I:%M %p"))
        self.after((60 - now.second) * 1000, self.update_time)

    def update_temp(self):
        """
        updates the temp display label and queues the next update just after 1 second
        """

        if reading := GPIOAPI.read_dht11():
            self.temp.set(f"{reading}°F")
        self.after(1000, self.update_temp)

    def sleep(self):
        """
        Puts the display to sleep by hiding the main window and turning off the HDMI output and queues a foreground job
        to wait for the wake-up signal from the display
        """

        # hide the main window and turn off the HDMI output
        self.winfo_toplevel().withdraw()
        run(["xrandr", "--output", "HDMI-1", "--off", "--output", "HDMI-2", "--off"])
        self.fg_job_manager.queue_display_sleep(lambda: self.after(0, self.wake))

    def wake(self):
        """
        wakes the display after a touch event by then re-enabling the HDMI output and showing the main window again.
        """

        self.winfo_toplevel().deiconify()
        run(["xrandr", "--output", "HDMI-1", "--auto", "--output", "HDMI-2", "--auto"])

    @staticmethod
    def close_patch_notes(patch_notes_frame):
        """
        closes the patch notes popup and deletes the patch notes file so it does not show up next boot
        """

        patch_notes_frame.destroy()
        remove("AppData/patch_notes.txt")
