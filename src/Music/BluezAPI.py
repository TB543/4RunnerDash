from pydbus import SystemBus
from time import sleep
from subprocess import run, PIPE
from os import environ
from time import strftime, gmtime


class BluezAPI:
    """
    A class to communicate with the connected Bluetooth devices via bluetooth.
    handles playback controls and can retrieve information about current track and playback status.
    additionally can handle volume controls
    """

    def __init__(self):
        """
        Initializes the AudioAPI by connecting to the system bus and retrieving the MediaPlayer1 interface.
        """

        self.bus = SystemBus()
        self.player = None
        self._title = None
        self._artist = None
        self._playback_ratio = 0
        self._elapsed_time_str = "00:00"
        self._remaining_time_str = "00:00"

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
            mngr = self.bus.get("org.bluez", "/")
            objects = mngr.GetManagedObjects()

            # finds player
            for path, interfaces in objects.items():
                if "org.bluez.MediaPlayer1" in interfaces:
                    self.player = self.bus.get("org.bluez", path)
                    return
        
        except:
            self.player = None
            
    # ========================================== PLAYBACK CONTROLS ==========================================

    def previous_track(self):
        try:
            self.player.Previous()
            self.player.Pause()
            sleep(.75)
            self.player.Play()
        except:
            self.update_player()

    def track_control(self):
        try:
            self.player.Pause() if self.player.Status == "playing" else self.player.Play()
        except:
            self.update_player()

    def next_track(self):
        try:
            self.player.Next()
        except:
            self.update_player()

    @staticmethod
    def set_volume(percent):
        run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{percent}%"])
        
    # ========================================== METADATA RETRIEVAL =========================================

    @property
    def title(self):
        try:
            self._title = self.player.Track["Title"]
        except:
            self.update_player()
        return self._title

    @property
    def artist(self):
        try:
            self._artist = self.player.Track["Artist"]
        except:
            self.update_player()
        return self._artist

    @property
    def elapsed_time_str(self):
        try:
            self._elapsed_time_str = strftime("%M:%S", gmtime(self.player.Position / 1000))
        except:
            self.update_player()
        return self._elapsed_time_str

    @property
    def playback_ratio(self):
        try:
            self._playback_ratio = self.player.Position / self.player.Track["Duration"]
        except:
            self.update_player()
        return self._playback_ratio

    @property
    def remaining_time_str(self):
        try:
            self._remaining_time_str = strftime("%M:%S", gmtime((self.player.Track["Duration"] - self.player.Position) / 1000))
        except:
            self.update_player()
        return self._remaining_time_str

    @property
    def playback_mode(self):
        try:
            return "❚❚" if self.player.Status == "playing" else "▶"
        except:
            self.update_player()
            return "▶"
        
    @property
    def volume(self):
        command = run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stdout=PIPE, text=True)
        result = command.stdout
        volume = result.split("%")
        volume = volume[0].split(" ")
        return int(volume[-1])
