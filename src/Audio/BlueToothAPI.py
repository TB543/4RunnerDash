from pydbus import SystemBus
from time import strftime, gmtime


class BlueToothAPI:
    """
    A class to communicate with the connected Bluetooth devices via bluetooth.
    handles playback controls and can retrieve information about current track and playback status.
    """

    def __init__(self):
        """
        Initializes the BlueToothAPI by connecting to the system bus and retrieving the MediaPlayer1 interface.
        """

        self.player = None
        self.update_player()
        self._title = "N/A"
        self._artist = "N/A"
        self._playback_ratio = 0
        self._elapsed_time_str = "00:00"
        self._remaining_time_str = "00:00"

    def update_player(self):
        """
        sets the player attribute
        """

        # gets bluetooth objects
        bus = SystemBus()
        mngr = bus.get("org.bluez", "/")
        objects = mngr.GetManagedObjects()

        # finds player
        for path, interfaces in objects.items():
            if "org.bluez.MediaPlayer1" in interfaces:
                self.player = bus.get("org.bluez", path)
                return
            
    # ========================================== PLAYBACK CONTROLS ==========================================

    def play(self):
        try:
            self.player.Play()
        except:
            self.update_player()

    def pause(self):
        try:
            self.player.Pause()
        except:
            self.update_player()

    def next_track(self):
        try:
            self.player.Next()
        except:
            self.update_player()

    def previous_track(self):
        try:
            self.player.Previous()
        except:
            self.update_player()

    # ========================================== METADATA RETRIEVAL =========================================

    @property
    def title(self):
        try:
            return self.player.Track["Title"]
        except:
            self.update_player()
            return self._title

    @property
    def artist(self):
        try:
            return self.player.Track["Artist"]
        except:
            self.update_player()
            return self._artist

    @property
    def playback_ratio(self):
        try:
            return self.player.Position / self.player.Track["Duration"]
        except:
            self.update_player()
            return self._playback_ratio

    @property
    def elapsed_time_str(self):
        try:
            return strftime("%M:%S", gmtime(self.player.Position / 1000))
        except:
            self.update_player()
            return self._elapsed_time_str

    @property
    def remaining_time_str(self):
        try:
            return strftime("%M:%S", gmtime((self.player.Track["Duration"] - self.player.Position) / 1000))
        except:
            self.update_player()
            return self._remaining_time_str

print(BlueToothAPI().artist)
