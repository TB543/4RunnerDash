from obd import Async, commands
from DataManagers.MileManager import MileManger
from AppData import TANK_CAPACITY


class OBDAPI(Async):
    """
    a class to communicate with the OBD-II interface of a vehicle.
    """

    def __init__(self, mpg, miles_until_empty, temp):
        """
        initializes the OBDAPI class.

        @param mpg: the callback function for updating the mpg
        @param miles_until_empty: the callback function for updating miles until empty
        @param temp: the callback function for updating the temperature
            ** note: temp callback should never raise errors, python-obd does not support error handling **

            ** note: all of these callbacks take 1 parameter for the new value **
        """

        # initializes the class and its fields
        super().__init__()
        self.mpg = mpg
        self.miles_until_empty = miles_until_empty
        self.speed_time = None

        # sets the codes to watch
        self.watch(commands.AMBIANT_AIR_TEMP, callback=lambda r: temp(f"{round(r.value.to('degF').magnitude)} °F" if r.value else "°F"))
        self.watch(commands.SPEED)
        self.watch(commands.FUEL_RATE)
        self.watch(commands.FUEL_LEVEL)
        self.watch(commands.FUEL_LEVEL, callback=lambda r: self.update_loop())
        self.start()

    def update_loop(self):
        """
        main update loop for the OBD-II interface.
        This method should be registered after all other commands are registered
        to ensure all commands are processed before this one.
        """

        # gets the values
        speed = self.query(commands.SPEED)
        fuel_rate = self.query(commands.FUEL_RATE)
        fuel_level = self.query(commands.FUEL_LEVEL)

        # handles the first response
        if self.speed_time is None:
            self.speed_time = speed.time
            return
        
        # updates the speed and calculates the time delta
        dt = speed.time - self.speed_time
        self.speed_time = speed.time

        # calculates required values
        mph = speed.value.to("mph").magnitude
        fuel_rate = fuel_rate.value.to("gallon / hour").magnitude
        mpg = mph / fuel_rate if fuel_rate != 0 else float("inf")
        miles_until_empty = mpg * fuel_level.value.to("ratio").magnitude * TANK_CAPACITY

        # sends updates to the UI
        try:
            self.mpg(round(mpg, 2))
            self.miles_until_empty(round(miles_until_empty, 2))
        except:
            pass
        MileManger.add_miles(mph * (dt / 3600))
        
    def get_codes(self):
        """
        runs diagnostics on the OBD-II interface and gets the codes.

        @return: a list of diagnostic trouble codes (DTCs) from the OBD-II interface.
            Each DTC is represented by a tuple containing the DTC code, and a description (if python-OBD has one)
        """

        with self.paused():
            codes = super(Async, self).query(commands.GET_DTC)
        return codes.value if codes.value else []

    def clear_codes(self):
        """
        clears the diagnostic trouble codes (DTCs) from the OBD-II interface.
        """

        with self.paused():
            super(Async, self).query(commands.CLEAR_DTC)

    def shutdown(self, root):
        """
        shuts down the OBD-II interface.

        @param root: the root window to update to ensure
            callbacks are processed while shutting down
        """

        # closes while preventing race conditions
        if self._Async__thread is not None:
            self._Async__running = False
            while self._Async__thread.is_alive():
                root.update()
            self._Async__thread = None

        self.close()
