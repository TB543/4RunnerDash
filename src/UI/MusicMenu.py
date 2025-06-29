from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkSlider, StringVar, DoubleVar
from AppData import MENU_ICON_FONT, MENU_LABEL_FONT, SONG_TITLE_FONT, SONG_ARTIST_FONT, SONG_TIME_FONT, TRACK_CONTROL_FONT, TRACK_SEEK_FONT
from Audio.BlueToothAPI import BlueToothAPI


class MusicMenu(CTkFrame):
    """
    a class to represent the music menu
    """

    FPS = 30
    FPS = int(1000 / FPS)

    def __init__(self, master, **kwargs):
        """
        Initializes the music menu frame.

        @param master: the parent widget
        @param kwargs: additional keyword arguments for CTkFrame
        """

        super().__init__(master, **kwargs)
        self.api = BlueToothAPI()
        self.fps_counter = None  # will be set on place

        # creates the container and main menu widgets
        container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu = CTkButton(self, text="Main Menu", font=MENU_LABEL_FONT, command=lambda: master.change_menu("main"))
        container.grid(row=1, column=1, columnspan=7, sticky="nsew")
        main_menu.grid(row=2, column=1, columnspan=7, pady=(0, 10), sticky="sew")

        # creates spacer widgets and sets grid layout
        self.rowconfigure(0, weight=1, uniform="row0")
        self.rowconfigure(2, weight=1, uniform="row0")
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = CTkButton(self, text="", font=MENU_ICON_FONT, fg_color="transparent", hover=False)
            spacer.grid(row=0, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates string vars to hold metadata
        self.title = StringVar(self)
        self.artist = StringVar(self)
        self.elapsed_time = StringVar(self)
        self.playback_ratio = DoubleVar(self)
        self.remaining_time = StringVar(self)
        self.player_status = StringVar(self)

        # creates metadata
        title = CTkLabel(container, textvariable=self.title, font=SONG_TITLE_FONT, anchor="w")
        artist = CTkLabel(container, textvariable=self.artist, font=SONG_ARTIST_FONT, anchor="w")
        elapsed_time = CTkLabel(container, textvariable=self.elapsed_time, font=SONG_TIME_FONT)
        progress_bar = CTkSlider(container, state="disabled", variable=self.playback_ratio)
        remaining_time = CTkLabel(container, textvariable=self.remaining_time, font=SONG_TIME_FONT)

        # creates playback control widgets
        previous_track = CTkButton(container, text="◀◀", font=TRACK_SEEK_FONT, corner_radius=float("inf"), command=self.api.previous_track)
        track_control = CTkButton(container, textvariable=self.player_status, font=TRACK_CONTROL_FONT, corner_radius=float("inf"), command=self.api.track_control)
        next_track = CTkButton(container, text="▶▶", font=TRACK_SEEK_FONT, corner_radius=float("inf"), command=self.api.next_track)
        previous_track.configure(width=previous_track.cget("height"))
        track_control.configure(width=track_control.cget("height") + 60, height=track_control.cget("height") + 20)
        next_track.configure(width=next_track.cget("height"))

        # places metadata widgets
        # todo image at row 0
        title.grid(row=1, column=1, columnspan=5, sticky="ew")
        artist.grid(row=2, column=1, columnspan=5, sticky="ew")
        elapsed_time.grid(row=3, column=1)
        progress_bar.grid(row=3, column=2, columnspan=3, sticky="ew")
        remaining_time.grid(row=3, column=5)

        # places playback control widgets
        previous_track.grid(row=4, column=2)
        track_control.grid(row=4, column=3)
        next_track.grid(row=4, column=4)

        # sets the grid layout of the container
        container.columnconfigure(0, weight=1)
        container.columnconfigure(2, weight=1)
        container.columnconfigure(4, weight=1)
        container.columnconfigure(6, weight=1)

    def update_metadata(self):
        """
        updates all of the metadata display widgets each frame
        """

        self.title.set(self.api.title)
        self.artist.set(self.api.artist)
        self.elapsed_time.set(self.api.elapsed_time_str)
        self.playback_ratio.set(self.api.playback_ratio)
        self.remaining_time.set(self.api.remaining_time_str)
        self.player_status.set(self.api.playback_mode)
        self.fps_counter = self.after(MusicMenu.FPS, self.update_metadata)

    def place(self, **kwargs):
        """
        overrides the place method to start the fps counter

        :param kwargs: the kwargs to pass to the super call
        """

        self.update_metadata()
        super().place(**kwargs)

    def place_forget(self):
        """
        overrides the place forget method to stop the fps counter
        """

        self.after_cancel(self.fps_counter)
        super().place_forget()
