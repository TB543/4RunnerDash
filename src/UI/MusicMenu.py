from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkSlider, StringVar, DoubleVar, IntVar, CTkImage
from Music import BluezAPI
from AppData import MENU_ICON_FONT, MENU_LABEL_FONT, SONG_TITLE_LABEL_KWARGS, SONG_ARTIST_LABEL_KWARGS, SONG_TIME_LABEL_KWARGS, TRACK_CONTROL_BUTTON_KWARGS, TRACK_SEEK_BUTTON_KWARGS, VOLUME_BUTTON_KWARGS, MAX_VOLUME
from DataManagers import AlbumArtManager


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

        # initializes fields
        super().__init__(master, **kwargs)
        self.art_manager = AlbumArtManager("AppData/default_album_art.png")
        self.art_job = None
        self.api = BluezAPI()
        self.fps_counter = None  # will be set on place

        # creates spacer widgets and sets grid layout
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        for col in range(1, 8, 2):
            spacer = CTkButton(self, text="", font=MENU_ICON_FONT, fg_color="transparent", hover=False, height=0)
            spacer.grid(row=1, column=col)
            self.columnconfigure(col + 1, weight=1)

        # creates the container and main menu widgets
        music_container = CTkFrame(self, fg_color=self.cget("fg_color"))
        main_menu = CTkButton(self, text="Main Menu", font=MENU_LABEL_FONT, command=lambda: master.change_menu("main"))
        music_container.grid(row=1, column=1, columnspan=7, sticky="nsew", padx=10, pady=10)
        main_menu.grid(row=0, column=1, columnspan=7, pady=(10, 0), sticky="new")
        music_container.grid_propagate(False)

        # creates vars to hold metadata
        self.title = StringVar(self, "N/A")
        self.artist = StringVar(self, "N/A")
        self.elapsed_time = StringVar(self)
        self.playback_ratio = DoubleVar(self)
        self.remaining_time = StringVar(self)
        self.player_status = StringVar(self)
        self.volume = IntVar(self, self.api.volume)
        self.image_container = CTkLabel(music_container, text="", image=CTkImage(self.art_manager.queue_job(None, None, None).result(), size=(200, 200)))
        self.volume.trace_add("write", lambda *args: self.api.set_volume(self.volume.get()))

        # creates metadata
        title = CTkLabel(music_container, textvariable=self.title, **SONG_TITLE_LABEL_KWARGS)
        artist = CTkLabel(music_container, textvariable=self.artist, **SONG_ARTIST_LABEL_KWARGS)
        elapsed_time = CTkLabel(music_container, textvariable=self.elapsed_time, **SONG_TIME_LABEL_KWARGS)
        progress_bar = CTkSlider(music_container, state="disabled", variable=self.playback_ratio)
        remaining_time = CTkLabel(music_container, textvariable=self.remaining_time, **SONG_TIME_LABEL_KWARGS)

        # creates playback control widgets
        previous_track = CTkButton(music_container, text="◀◀", command=self.api.previous_track, **TRACK_SEEK_BUTTON_KWARGS)
        track_control = CTkButton(music_container, textvariable=self.player_status, command=self.api.track_control, **TRACK_CONTROL_BUTTON_KWARGS)
        next_track = CTkButton(music_container, text="▶▶", command=self.api.next_track, **TRACK_SEEK_BUTTON_KWARGS)

        # creates volume container
        volume_container = CTkFrame(music_container, fg_color=self.cget("fg_color"))
        volume_up = CTkButton(volume_container, text="🔊", command=lambda: self.volume.set(self.volume.get() + 5), **VOLUME_BUTTON_KWARGS)
        volume_slider = CTkSlider(volume_container, from_=0, to=MAX_VOLUME, variable=self.volume, orientation="vertical")
        volume_down = CTkButton(volume_container, text="🔉", command=lambda: self.volume.set(self.volume.get() - 5 if self.volume.get() - 5 >= 0 else 0), **VOLUME_BUTTON_KWARGS)

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

        # places volume controls
        volume_up.grid(row=0, column=1, sticky="s")
        volume_slider.grid(row=1, column=1, pady=5)
        volume_down.grid(row=2, column=1, sticky="n")
        volume_container.rowconfigure(0, weight=1, uniform="row0")
        volume_container.rowconfigure(2, weight=1, uniform="row0")
        volume_container.columnconfigure(0, weight=1)
        volume_container.columnconfigure(2, weight=1)
        volume_container.grid(row=0, column=0, rowspan=5, sticky="nsew")

        # sets the grid layout of the container
        music_container.rowconfigure(0, weight=1)
        music_container.rowconfigure(4, weight=1)
        music_container.columnconfigure(0, weight=1, uniform="col0")
        music_container.columnconfigure(2, weight=1)
        music_container.columnconfigure(4, weight=1)
        music_container.columnconfigure(6, weight=1, uniform="col0")
        title.grid_propagate(False)
        artist.grid_propagate(False)

    def update_metadata(self):
        """
        updates all of the metadata display widgets each frame
        """

        # sets metadata
        old_data = (self.title.get(), self.artist.get())
        self.playback_ratio.set(self.api.playback_ratio)  # fetched first to update player and return 00:00 when needed
        title, artist = self.api.title, self.api.artist   # this way title is not returned as None
        self.title.set(title if title else "N/A")
        self.artist.set(artist if artist else "N/A")
        self.elapsed_time.set(self.api.elapsed_time_str)
        self.remaining_time.set(self.api.remaining_time_str)
        self.player_status.set(self.api.playback_mode)
        self.fps_counter = self.after(MusicMenu.FPS, self.update_metadata)

        # updates image
        if old_data != (self.title.get(), self.artist.get()):
            self.art_job = self.art_manager.queue_job(title, artist, self.api.album)
        if self.art_job and self.art_job.done():
            self.image_container.configure(image=CTkImage(self.art_job.result(), size=(200, 200)))
            self.art_job = None

    def place(self, **kwargs):
        """
        overrides the place method to start the fps counter

        :param kwargs: the kwargs to pass to the super call
        """

        super().place(**kwargs)
        self.update_metadata()

    def place_forget(self):
        """
        overrides the place forget method to stop the fps counter
        """

        super().place_forget()
        self.after_cancel(self.fps_counter)

    def destroy(self):
        """
        overrides the destroy method to also shut down the album art job manager
        """

        self.art_manager.shutdown()
        super().destroy()
