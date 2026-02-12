from obd import Async, commands
from DataManagers.MileManager import MileManger
from AppData import TANK_CAPACITY
from logging import disable, CRITICAL


class OBDAPI(Async):
    """
    a class to communicate with the OBD-II interface of a vehicle.
    """

    # disables obd logging
    disable(CRITICAL)

    def __init__(self, root, job_manager, mpg, miles_until_empty):
        """
        initializes the OBDAPI class.

        @param root: the root window to update to prevent deadlocks
        @param job_manager: handles connecting to the OBD interface in background threads
        @param mpg: the callback function for updating the mpg
        @param miles_until_empty: the callback function for updating miles until empty
            ** note: all of these callbacks take 1 parameter for the new value **
        """

        # initializes fields
        self.root = root
        self.job_manager = job_manager
        self.mpg = mpg
        self.miles_until_empty = miles_until_empty
        self.speed_time = None
        self.job_manager.queue_obd_connection_job(self, root)

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

        # fails if bg job manager has not finished connecting to obd
        try:
            with self.paused():
                codes = super(Async, self).query(commands.GET_DTC)
            return codes.value if codes.value else []
        
        # returns no codes on failure
        except:
            return []

    def clear_codes(self):
        """
        clears the diagnostic trouble codes (DTCs) from the OBD-II interface.
        """


        # fails if bg job manager has not finished connecting to obd
        try:
            with self.paused():
                super(Async, self).query(commands.CLEAR_DTC)

        # do nothing on failure
        except:
            return

    def stop(self):
        """
        overrides the stop method to prevent deadlocks:
            GUI waiting for async thread to join
            async thread waiting to update GUI
        """

        # fails if bg job manager has not finished connecting to obd
        try:
            if self._Async__thread is not None:
                self._Async__running = False

                # update UI until thread finishes to prevent deadlock
                while self._Async__thread.is_alive():
                    self.root.update()
                self._Async__thread = None

        # do nothing on failure, there is nothing to stop
        except:
            return

    def run(self):
        """
        overrides the superclass run method to ensure if connection to car fails, it retries
        """

        super().run()
        if not self.is_connected():
            self.job_manager.queue_obd_connection_job(self, self.root)

    def shutdown(self):
        """
        shuts down the OBD-II interface.
        """

        self.close()
        MileManger.save()
