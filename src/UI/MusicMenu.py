from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkSlider, StringVar, IntVar
from AppData import LABEL_FONT, SONG_TITLE_FONT, SONG_ARTIST_FONT
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

        # creates string vars
        self.title = StringVar(self, self.api.title)
        self.artist = StringVar(self, self.api.artist)
        self.elapsed_time = StringVar(self, self.api.elapsed_time_str)
        self.playback_ratio = IntVar(self, self.api.playback_ratio)
        self.remaining_time = StringVar(self, self.api.remaining_time_str)
        self.player_status = StringVar(self, self.api.playback_mode)

        # creates metadata
        title = CTkLabel(self, textvariable=self.title, font=SONG_TITLE_FONT)
        artist = CTkLabel(self, textvariable=self.artist, font=SONG_ARTIST_FONT)
        elapsed_time = CTkLabel(self, textvariable=self.elapsed_time, font=LABEL_FONT)
        progress_bar = CTkSlider(self, state="disabled", variable=self.playback_ratio)
        remaining_time = CTkLabel(self, textvariable=self.remaining_time, font=LABEL_FONT)

        # creates playback control widgets
        previous_track = CTkButton(self, text="⏮", font=LABEL_FONT, fg_color="transparent", hover=False, command=self.api.previous_track)
        toggle_play_pause = CTkButton(self, textvariable=self.player_status, font=LABEL_FONT, corner_radius=float("inf"), command=self.api.toggle_play_pause)
        next_track = CTkButton(self, text="⏭", font=LABEL_FONT, fg_color="transparent", hover=False, command=self.api.next_track)
        main_menu = CTkButton(self, text="Main Menu", font=LABEL_FONT, command=lambda: master.change_menu("main"))

        # places metadata widgets
        # todo image at row 0
        title.grid(row=1, column=1, columnspan=5, sticky="w")
        artist.grid(row=2, column=1, columnspan=5, sticky="w")
        elapsed_time.grid(row=3, column=1, sticky="e")
        progress_bar.grid(row=3, column=2, columnspan=3, sticky="ew")
        remaining_time.grid(row=3, column=5, sticky="w")

        # places playback control widgets
        previous_track.grid(row=4, column=2, sticky="ne")
        toggle_play_pause.grid(row=4, column=3, sticky="n")
        next_track.grid(row=4, column=4)
        main_menu.grid(row=5, column=1, columnspan=5, pady=(0, 10), sticky="sew")

        # sets the grid layout
        self.grid_rowconfigure(0, weight=1, uniform="row0")
        self.grid_rowconfigure(5, weight=1, uniform="row0")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(6, weight=1)

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


from customtkinter import CTk
window = MusicMenu(CTk())
window.master.geometry(f"{1040}x{600}+0+0")
window.pack(fill="both", expand=True)
window.master.mainloop()
