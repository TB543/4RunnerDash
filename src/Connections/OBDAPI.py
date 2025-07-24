from obd import Async, commands
from DataManagers.MileManager import MileManger
from AppData import TANK_CAPACITY


class OBDAPI(Async):
    """
    a class to communicate with the OBD-II interface of a vehicle.
    """

    def __init__(self, mpg, miles_until_empty, temp, root):
        """
        initializes the OBDAPI class.

        @param mpg: a DoubleVar to hold the miles per gallon value
        @param miles_until_empty: a DoubleVar to hold the miles until empty value
        @param temp: a StringVar to hold the temperature
        @param root: a tkinter widget for scheduling variable updates
        """

        # initializes the class and its fields
        super().__init__()
        self.mpg = mpg
        self.miles_until_empty = miles_until_empty
        self.root = root
        self.speed_time = None

        # sets the codes to watch
        self.watch(commands.AMBIANT_AIR_TEMP, callback=lambda r: self.root.after(0, lambda: temp.set(f"{round(r.to('degF').magnitude)} °F")))
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
        self.root.after(0, lambda: self.mpg.set(round(mpg, 2)))
        self.root.after(0, lambda: self.miles_until_empty.set(round(miles_until_empty, 2)))
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

    def shutdown(self):
        """
        shuts down the OBD-II interface.
        """

        self.close()
