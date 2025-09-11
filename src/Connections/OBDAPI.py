from obd import Async, commands
from DataManagers.MileManager import MileManger
from AppData import TANK_CAPACITY


class OBDAPI(Async):
    """
    a class to communicate with the OBD-II interface of a vehicle.
    """

    def __init__(self, root, mpg, miles_until_empty, temp):
        """
        initializes the OBDAPI class.

        @param root: the root window to update to prevent deadlocks
        @param mpg: the callback function for updating the mpg
        @param miles_until_empty: the callback function for updating miles until empty
        @param temp: the callback function for updating the temperature
            ** note: all of these callbacks take 1 parameter for the new value **
        """

        # attempts to connect to OBD scanner, does nothing if fails
        try:
            super().__init__()
        except:
            super().__init__("No OBD Connection")

        # initializes fields
        self.root = root
        self.mpg = mpg
        self.miles_until_empty = miles_until_empty
        self.temp = temp
        self.speed_time = None

        # sets the codes to watch
        self.watch(commands.SPEED)
        self.watch(commands.MAF)
        self.watch(commands.FUEL_LEVEL)
        self.watch(commands.INTAKE_TEMP, callback=lambda r: self.update_loop())
        self.start()

    def update_loop(self):
        """
        main update loop for the OBD-II interface.
        This method should be registered after all other commands are registered
        to ensure all commands are processed before this one.
        """

        # gets the values
        speed = self.query(commands.SPEED)
        maf = self.query(commands.MAF)
        fuel_level = self.query(commands.FUEL_LEVEL)
        temp = self.query(commands.INTAKE_TEMP)

        # handles the first response
        if self.speed_time is None:
            self.speed_time = speed.time
            return
        
        # updates the speed and calculates the time delta
        dt = speed.time - self.speed_time
        self.speed_time = speed.time

        # calculates required values
        mph = speed.value.to("mph").magnitude if speed.value is not None else 0
        mpg = mph / (maf.value.magnitude * .0805) if maf.value is not None else 0
        miles_until_empty = mpg * fuel_level.value.to("ratio").magnitude * TANK_CAPACITY if fuel_level.value is not None else 0
        temp = round(temp.value.to('degF').magnitude) if temp.value is not None else ""

        # sends updates to the UI
        try:
            self.mpg(round(mpg, 2))
            self.miles_until_empty(round(miles_until_empty, 2))
            self.temp(f"{temp} °F")
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

    def stop(self):
        """
        overrides the stop method to prevent deadlocks:
            GUI waiting for async thread to join
            async thread waiting to update GUI
        """

        if self._Async__thread is not None:
            self._Async__running = False
            while self._Async__thread.is_alive():
                self.root.update()
            self._Async__thread = None

    def shutdown(self):
        """
        shuts down the OBD-II interface.

        @param root: the root window to update to ensure
            callbacks are processed while shutting down
        """

        self.close()
