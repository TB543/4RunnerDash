from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkSlider, StringVar, DoubleVar, IntVar
from AppData import MENU_ICON_FONT, MENU_LABEL_FONT, SONG_TITLE_LABEL_KWARGS, SONG_ARTIST_LABEL_KWARGS, SONG_TIME_LABEL_KWARGS, TRACK_CONTROL_BUTTON_KWARGS, TRACK_SEEK_BUTTON_KWARGS, VOLUME_BUTTON_KWARGS, MAX_VOLUME
from Audio.AudioAPI import AudioAPI


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
        self.api = AudioAPI()
        self.fps_counter = None  # will be set on place

        # creates spacer widgets and sets grid layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = CTkButton(self, text="", font=MENU_ICON_FONT, fg_color="transparent", hover=False)
            spacer.grid(row=0, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates the container and main menu widgets
        container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu = CTkButton(self, text="Main Menu", font=MENU_LABEL_FONT, command=lambda: master.change_menu("main"))
        container.grid(row=0, column=1, columnspan=7, sticky="nsew", padx=10, pady=10)
        main_menu.grid(row=1, column=1, columnspan=7, pady=(0, 10), sticky="sew")
        container.grid_propagate(False)

        # creates string vars to hold metadata
        self.title = StringVar(self)
        self.artist = StringVar(self)
        self.elapsed_time = StringVar(self)
        self.playback_ratio = DoubleVar(self)
        self.remaining_time = StringVar(self)
        self.player_status = StringVar(self)
        self.volume = IntVar(self, 50)
        self.volume.trace_add("write", lambda *args: self.api.set_volume(self.volume.get()))

        # creates metadata
        title = CTkLabel(container, textvariable=self.title, **SONG_TITLE_LABEL_KWARGS)
        artist = CTkLabel(container, textvariable=self.artist, **SONG_ARTIST_LABEL_KWARGS)
        elapsed_time = CTkLabel(container, textvariable=self.elapsed_time, **SONG_TIME_LABEL_KWARGS)
        progress_bar = CTkSlider(container, state="disabled", variable=self.playback_ratio)
        remaining_time = CTkLabel(container, textvariable=self.remaining_time, **SONG_TIME_LABEL_KWARGS)

        # creates playback control widgets
        previous_track = CTkButton(container, text="◀◀", command=self.api.previous_track, **TRACK_SEEK_BUTTON_KWARGS)
        track_control = CTkButton(container, textvariable=self.player_status, command=self.api.track_control, **TRACK_CONTROL_BUTTON_KWARGS)
        next_track = CTkButton(container, text="▶▶", command=self.api.next_track, **TRACK_SEEK_BUTTON_KWARGS)
        volume_up = CTkButton(container, text="↑", command=lambda: self.volume.set(self.volume.get() + 5), **VOLUME_BUTTON_KWARGS)
        volume_slider = CTkSlider(container, from_=0, to=MAX_VOLUME, variable=self.volume, orientation="vertical")
        volume_down = CTkButton(container, text="↓", command=lambda: self.volume.set(self.volume.get() - 5 if self.volume.get() - 5 >= 0 else 0), **VOLUME_BUTTON_KWARGS)

        # places metadata widgets
        # todo image at row 0 to 1
        title.grid(row=2, column=1, columnspan=5, sticky="ew")
        artist.grid(row=3, column=1, columnspan=5, sticky="ew")
        elapsed_time.grid(row=4, column=1)
        progress_bar.grid(row=4, column=2, columnspan=3, sticky="ew")
        remaining_time.grid(row=4, column=5)

        # places playback control widgets
        previous_track.grid(row=5, column=2)
        track_control.grid(row=5, column=3)
        next_track.grid(row=5, column=4)
        volume_up.grid(row=0, column=0, sticky="w", pady=(0, 5))
        volume_slider.grid(row=1, column=0, rowspan=4, sticky="nsw", padx=4)
        volume_down.grid(row=5, column=0, sticky="w")

        # sets the grid layout of the container
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1, uniform="col0")
        container.columnconfigure(2, weight=1)
        container.columnconfigure(4, weight=1)
        container.columnconfigure(6, weight=1, uniform="col0")
        title.grid_propagate(False)
        artist.grid_propagate(False)

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
