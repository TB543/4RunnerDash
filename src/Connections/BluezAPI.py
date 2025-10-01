from time import sleep
from time import strftime, gmtime
from DataManagers.BGJobManager import BGJobManager
try:
    from pydbus import SystemBus
except ModuleNotFoundError:
    from Dev.Imports.pydbus import *


class BluezAPI(SystemBus):
    """
    A class to communicate with the connected Bluetooth devices via bluetooth.
    handles playback controls and can retrieve information about current track and playback status.
    """

    def __init__(self):
        """
        Initializes the AudioAPI by connecting to the system bus and retrieving the MediaPlayer1 interface.
        """

        # initializes the fields
        super().__init__()
        self.player = None
        self.art_manager = BGJobManager()
        self._title = None
        self._artist = None
        self._playback_ratio = 0
        self._elapsed_time_str = "00:00"
        self._remaining_time_str = "00:00"

        # gets album art
        self.update_player()
        self.art_job = self.art_manager.queue_job(self.title, self.artist, self.album)
        self.art_job.result()
        self.last_property_params = None

        # sets listener for track change
        self.subscribe(
            iface="org.freedesktop.DBus.Properties",
            signal="PropertiesChanged",
            signal_fired=lambda *args: self.update_album_art(args[4][1])
        )

    def update_album_art(self, params):
        """
        updates album art if track changes

        @param params: the parameters for the property change
        """

        if "Track" in params and self.last_property_params != (params["Track"]["Title"], params["Track"]["Artist"]):
            self.last_property_params = (params["Track"]["Title"], params["Track"]["Artist"])
            self.art_job = self.art_manager.queue_job(self.title, self.artist, self.album)

    def update_player(self):
        """
        sets the player attribute
        """

        # resets metadata
        self._title = None
        self._artist = None
        self._playback_ratio = 0
        self._elapsed_time_str = "00:00"
        self._remaining_time_str = "00:00"

        # gets bluetooth objects
        try:
            mngr = self.get("org.bluez", "/")
            objects = mngr.GetManagedObjects()

            # finds player
            for path, interfaces in objects.items():
                if "org.bluez.MediaPlayer1" in interfaces:
                    self.player = self.get("org.bluez", path)
                    return

        except:
            self.player = None

    def shutdown(self):
        """
        shuts down the album art manager
        """

        self.art_manager.shutdown(cancel_futures=True)

    # ========================================== PLAYBACK CONTROLS ==========================================

    def previous_track(self):
        """
        attempts to skip to the previous track.
        if it fails, it attempts to update the player.
        """

        try:
            self.player.Previous()
            self.player.Pause()
            sleep(.75)
            self.player.Play()
        except:
            self.update_player()

    def track_control(self):
        """
        attempts to toggle play/pause.
        if it fails, it attempts to update the player.
        """

        try:
            self.player.Pause() if self.player.Status == "playing" else self.player.Play()
        except:
            self.update_player()

    def next_track(self):
        """
        attempts to skip to the next track.
        if it fails, it attempts to update the player.
        """

        try:
            self.player.Next()
        except:
            self.update_player()

    # ========================================== METADATA RETRIEVAL =========================================

    @property
    def title(self):
        """
        attempts to get the title of the current track.
        attempts to update the player if it fails.

        @return: the title of the current track
        """

        try:
            self._title = self.player.Track["Title"]
        except:
            self.update_player()
        return self._title

    @property
    def artist(self):
        """
        attempts to get the artist of the current track.
        attempts to update the player if it fails.

        @return: the artist of the current track
        """

        try:
            self._artist = self.player.Track["Artist"]
        except:
            self.update_player()
        return self._artist

    @property
    def album(self):
        """
        attempts to get the album of the current track.

        @return: the album of the current track
        """

        try:
            return self.player.Track["Album"]
        except:
            return None

    @property
    def album_art(self):
        """
        attempts to get the album art of the current track.
        only retrieves the art if the queued job has completed
        additionally this method will only return the art for
        the current track once to avoid repeat calling the expensive job

        @return: the album of the current track
        """

        art = None
        if self.art_job and self.art_job.done():
            art = self.art_job.result()
            self.art_job = None
        return art

    @property
    def elapsed_time_str(self):
        """
        attempts to get the elapsed time of the current track.
        attempts to update the player if it fails

        @return: the elapsed time of the current track
        """

        try:
            self._elapsed_time_str = strftime("%M:%S", gmtime(self.player.Position / 1000))
        except:
            self.update_player()
        return self._elapsed_time_str

    @property
    def playback_ratio(self):
        """
        attempts to get the playback ratio of the current track.
        attempts to update the player if it fails

        @return: a value between 0 and 1 to represent the playback ratio
        """

        try:
            self._playback_ratio = self.player.Position / self.player.Track["Duration"]
        except:
            self.update_player()
        return self._playback_ratio

    @property
    def remaining_time_str(self):
        """
        attempts to get the remaining time of the current track.
        attempts to update the player if it fails

        @return: the remaining time of the current track
        """

        try:
            self._remaining_time_str = strftime("%M:%S", gmtime((self.player.Track["Duration"] - self.player.Position) / 1000))
        except:
            self.update_player()
        return self._remaining_time_str

    @property
    def playback_mode(self):
        """
        attempts to get the player status.
        attempts to update the player if it fails

        @return: a string to represent either "playing" or "paused"
        """

        try:
            return "❚❚" if self.player.Status == "playing" else "▶"
        except:
            self.update_player()
            return "▶"
