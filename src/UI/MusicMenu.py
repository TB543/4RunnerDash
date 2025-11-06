from customtkinter import CTkFrame, CTkLabel, CTkSlider, StringVar, DoubleVar, CTkImage
from Dev.TSCTkButton import TSCTkButton
from AppData import FPS


class MusicMenu(CTkFrame):
    """
    a class to represent the music menu
    """

    FPS = int(1000 / FPS)

    def __init__(self, master, audio_api, **kwargs):
        """
        Initializes the music menu frame.

        @param master: the parent widget
        @param audio_api: the api for the audio system
        @param kwargs: additional keyword arguments for CTkFrame
        """

        # initializes fields
        super().__init__(master, **kwargs)
        self.audio_api = audio_api
        self.fps_counter = None  # will be set on place

        # creates spacer widgets and sets grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = TSCTkButton(self, text="", font=("Arial", 100), fg_color="transparent", hover=False, height=0)
            spacer.grid(row=1, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates the container and main menu widgets
        music_container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu = TSCTkButton(self, text="Main Menu", font=("Arial", 20), command=lambda: master.change_menu("main"))
        music_container.grid(row=1, column=1, columnspan=7, sticky="nsew", pady=10)
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        music_container.grid_propagate(False)

        # creates vars to hold metadata
        self.title = StringVar(self, "N/A")
        self.artist = StringVar(self, "N/A")
        self.elapsed_time = StringVar(self)
        self.playback_ratio = DoubleVar(self)
        self.remaining_time = StringVar(self)
        self.player_status = StringVar(self)
        self.image_container = CTkLabel(music_container, text="", image=CTkImage(self.audio_api.album_art, size=(200, 200)))

        # creates metadata
        title = CTkLabel(music_container, textvariable=self.title, height=15, font=("Arial", 12, "bold"), anchor="w")
        artist = CTkLabel(music_container, textvariable=self.artist, height=10, font=("Arial", 10), anchor="w")
        elapsed_time = CTkLabel(music_container, textvariable=self.elapsed_time, height=8, font=("Arial", 8))
        progress_bar = CTkSlider(music_container, state="disabled", variable=self.playback_ratio)
        remaining_time = CTkLabel(music_container, textvariable=self.remaining_time, height=8, font=("Arial", 8))

        # creates playback control widgets
        previous_track = TSCTkButton(music_container, text="◀◀", command=self.audio_api.previous_track, width=50, height=20, font=("Arial", 10), corner_radius=float("inf"))
        track_control = TSCTkButton(music_container, textvariable=self.player_status, command=self.audio_api.track_control, width=75, height=35, font=("Arial", 15), corner_radius=float("inf"))
        next_track = TSCTkButton(music_container, text="▶▶", command=self.audio_api.next_track, width=50, height=20, font=("Arial", 10), corner_radius=float("inf"))

        # places metadata widgets
        self.image_container.grid(row=0, column=2, columnspan=3, pady=(0, 6))
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
        music_container.rowconfigure(0, weight=1)
        music_container.rowconfigure(4, weight=1)
        music_container.columnconfigure(0, weight=1, uniform="col0")
        music_container.columnconfigure(2, weight=1)
        music_container.columnconfigure(4, weight=1)
        music_container.columnconfigure(6, weight=1, uniform="col0")
        title.grid_propagate(False)
        artist.grid_propagate(False)

    def update_loop(self):
        """
        updates all of the metadata display widgets each frame
        """

        # sets metadata
        self.playback_ratio.set(self.audio_api.playback_ratio)  # fetched first to update player and return 00:00 when needed
        title, artist = self.audio_api.title, self.audio_api.artist   # this way title is not returned as None
        self.title.set(title if title else "N/A")
        self.artist.set(artist if artist else "N/A")
        self.elapsed_time.set(self.audio_api.elapsed_time_str)
        self.remaining_time.set(self.audio_api.remaining_time_str)
        self.player_status.set(self.audio_api.playback_mode)

        # queues next update and updates album art if available
        self.fps_counter = self.after(MusicMenu.FPS, self.update_loop)
        if (art := self.audio_api.album_art):
            self.image_container.configure(image=CTkImage(art, size=(200, 200)))

    def place(self, **kwargs):
        """
        overrides the place method to start the fps counter

        :param kwargs: the kwargs to pass to the super call
        """

        super().place(**kwargs)
        self.update_loop()

    def place_forget(self):
        """
        overrides the place forget method to stop the fps counter
        """

        self.after_cancel(self.fps_counter)
        super().place_forget()
