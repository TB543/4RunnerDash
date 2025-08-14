from RPi.GPIO import setmode, BCM, setup, IN, OUT, HIGH, add_event_detect, FALLING, BOTH, input as read
from subprocess import run
from AppData import IGNORE_SHUTDOWN


class GPIOAPI:
    """
    a class to handle communication with the GPIO pins. implements the following:
        -> safe shutdown
        -> amp control
        -> system appearance mode detection (based on car head lights)
    """

    # initializes gpio settings
    setmode(BCM)
    setup(12, IN)
    setup(13, IN)
    setup(25, OUT, initial=HIGH)

    def __init__(self, shutdown, dimmer, lock):
        """
        initializes an instance of the GPIO api

        @param shutdown: a callback function to run before the shutdown command is issued
        @param dimmer: a callback function to run when the dimmer wire is switched
            takes 1 parameter, for the new state of the dimmer: 0 for low, 1 for high
        @param lock: the thread lock to hold while executing the shutdown command
            this will prevent premature exit of the program
        """

        # shutdown command
        self.lock = lock
        if not IGNORE_SHUTDOWN:
            add_event_detect(12, FALLING, lambda e: self.shutdown(shutdown))
            self.shutdown(shutdown) if read(12) == 0 else None

        # dimmer command
        add_event_detect(13, BOTH, lambda e: dimmer(read(13)))
        dimmer(read(13))

    def shutdown(self, callback):
        """
        runs the specified shutdown callback and shuts down the pi

        @param callback: the shutdown callback to run
        """

        with self.lock:
            try:
                callback()
            except:
                pass
            run(["../stop_backend.sh"])
            run(["sudo", "shutdown", "-h", "now"])
