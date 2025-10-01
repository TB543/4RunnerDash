from subprocess import run, PIPE, Popen
from AppData import MAX_VOLUME
from time import sleep
from sys import argv
try:
    from RPi.GPIO import setmode, BCM, setup, IN, OUT, add_event_detect, FALLING, BOTH, input as read, output, PUD_UP
    from dht11 import DHT11
except ModuleNotFoundError:
    from Dev.Imports.GPIO import *
    from Dev.Imports.dht11 import *


class GPIOAPI:
    """
    a class to handle communication with the GPIO pins. implements the following:
        -> safe shutdown
        -> amp control
        -> system appearance mode detection (based on car headlights)
    """

    # CarPiHat pins
    setmode(BCM)
    setup(12, IN)
    setup(13, IN)
    setup(25, OUT, initial=1)
    setup(27, OUT, initial=0)  # start off to avoid crackling on boot up

    # volume rotary encoder pins
    setup(26, IN)
    setup(6, IN)
    setup(5, IN, pull_up_down=PUD_UP)

    dht = DHT11(4)

    def __init__(self, shutdown, dimmer, volume, lock):
        """
        initializes an instance of the GPIO api

        @param shutdown: a callback function to run before the shutdown command is issued
        @param dimmer: a callback function to run when the dimmer wire is switched
            takes 1 parameter, for the new state of the dimmer: 0 for low, 1 for high
        @param volume: a callback function to run when the volume is changed
            takes 1 parameter, for the new volume % between 0 and 1
        @param lock: the thread lock to hold while executing the shutdown command
            this will prevent premature exit of the program
        """

        # get current volume
        try:
            command = run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stdout=PIPE, text=True)
            result = command.stdout
            result = result.split("%")
            result = result[0].split(" ")
            self.volume = int(result[-1])
        except:
            self.volume = MAX_VOLUME // 2

        # volume control
        output(27, 1)  # amp on
        add_event_detect(26, BOTH, lambda e: self.rotary_encoder_rotate(volume), bouncetime=2)
        add_event_detect(5, BOTH, lambda e: self.rotary_encoder_press(), bouncetime=25)

        # shutdown command
        self.lock = lock
        if len(argv) < 2 or argv[1] != "dev":
            add_event_detect(12, FALLING, lambda e: self.shutdown(shutdown))
            self.shutdown(shutdown) if read(12) == 0 else None

        # dimmer command
        add_event_detect(13, BOTH, lambda e: dimmer(read(13)))
        dimmer(read(13))

    def rotary_encoder_rotate(self, volume):
        """
        called when the volume rotary encoder is rotated. Adjusts volume accordingly.

        @param volume: the volume callback
        """

        # readings
        clk = read(26)
        dt = read(6)

        # volume down
        if clk == dt and self.volume > 0:
            self.volume -= 1
            Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-1%"])

        # volume up
        elif clk != dt and self.volume < MAX_VOLUME:
            self.volume += 1
            Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+1%"])

        # displays volume to screen
        volume(self.volume / MAX_VOLUME)

    @staticmethod
    def rotary_encoder_press():
        """
        called when the volume rotary encoder is pressed
        """

        if read(5) == 0:
            output(27, 0 if read(27) == 1 else 1)

    @classmethod
    def read_dht11(cls):
        """
        reads the dht11 sensor

        @return: the temperature in f
        """

        reading = cls.dht.read()
        if reading.is_valid():
            return (reading.temperature * 1.8) + 32

    def shutdown(self, callback):
        """
        runs the specified shutdown callback and shuts down the pi

        @param callback: the shutdown callback to run
        """

        # ensures pi stays on throughout short power loss (switch from battery to engine power)
        sleep(5)
        if read(12) == 1:
            return

        # gracefully shuts down
        with self.lock:
            try:
                callback()
            except:
                pass
            run(["sudo", "shutdown", "-h", "now"])
