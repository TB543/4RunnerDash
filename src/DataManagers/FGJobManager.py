from concurrent.futures import ThreadPoolExecutor
from time import time
from subprocess import Popen
from Connections.NavigationAPI import NavigationAPI
try:
    from evdev.ecodes import BTN_TOUCH
except ModuleNotFoundError:
    from Dev.Imports.evdev import *


class FGJobManager(ThreadPoolExecutor):
    """
    a class to manage foreground jobs such as the following:
        --> display sleep job
        --> address search jobs
        --> routing jobs
    """

    def __init__(self, touch_screen):
        """
        creates a new FGJobManager instance

        @param touch_screen: the touch screen display to listen to for events in the display sleep job
        """

        super().__init__()
        self.touch_screen = touch_screen
        self.address_search_future = None
        self.running_app = None
        self._ignore_shutdown = False
        self.shutdown_callback = None

    def queue_display_sleep(self, wake):
        """
        creates a display sleep job. ie wait for input to wake up the display

        @param wake: the function to call to wake up the display when an input is given
        """

        future = self.submit(self.display_sleep_job)
        future.add_done_callback(lambda f: wake())

    def queue_address_search(self, address, done):
        """
        creates an address search job

        @param address: the address to search
        @param done: the callback function to call when the address search is done

        @return: a future object for accessing the coordinates of the address
        """

        self.address_search_future.cancel() if self.address_search_future else None
        future = self.submit(lambda: FGJobManager.address_search_job(address))
        future.add_done_callback(lambda f: done(address, f.result()) if not f.cancelled() else None)
        self.address_search_future = future

    def queue_routing(self, destination, done):
        """
        creates a routing job

        @param destination: the coordinates of the destination
        @param done: the callback function to call when the routing is done

        @return: a future object for accessing the calculated route later
        """

    def start_application(self, callback, command, cwd=None, ignore_shutdown=False):
        """
        start an application and waits for it to finish
        this program will be hidden but continue running in the background until app has exited

        @param callback: the function to call when the application has exited
        @param command: the command that will be executed to start the app
        @param cwd: the current working directory of the app
        @param ignore_shutdown: whether to ignore ignition shutdown while app is running
        """

        # if app fails to launch print a message
        try:
            self.running_app = Popen(command, cwd=cwd, shell=True)
        except:
            self.running_app = Popen("echo invalid command to launch app", cwd=cwd, shell=True)

        # starts job to wait for app to exit
        self.shutdown_callback = None
        self._ignore_shutdown = ignore_shutdown
        future = self.submit(self.application_job)
        future.add_done_callback(lambda f: callback())
        future.add_done_callback(lambda f: self.shutdown_callback() if self.shutdown_callback else None)

    def display_sleep_job(self):
        """
        the job for display sleep, waits for the user to tap the display to wake it up
        """

        # wait for next touch event
        start = time()
        for event in self.touch_screen.read_loop():
            if event.code == BTN_TOUCH and event.value == 1 and event.timestamp() > start:
                break

        # wait for the next release event
        for event in self.touch_screen.read_loop():
            if event.code == BTN_TOUCH and event.value == 0:
                break

    @staticmethod
    def address_search_job(address):
        """
        the job for address search, queries the navigation api and waits for the response

        @param address: the address to search

        @return: the response from the navigation api containing the coordinates of the address
        """

        return NavigationAPI.geocode(address)

    @staticmethod
    def routing_job(destination):
        """
        the job for routing, queries the navigation api and waits for the response

        @param destination: the coordinates of the destination

        @return: the response from the navigation api containing the route to the destination
        """

        return NavigationAPI.navigate(destination)

    def application_job(self):
        """
        waits for the running application to exit before calling the done callback
        """

        self.running_app.wait()
        self._ignore_shutdown = False

    def ignore_shutdown(self, shutdown):
        """
        checks to see if an application is running and if it is configured to ignore the ignition shutdown

        @param shutdown: the function to call when application has exited and shutdown sequence can begin
        """

        self.shutdown_callback = shutdown if self._ignore_shutdown else None
        return self._ignore_shutdown

    def shutdown(self, wait = True, *, cancel_futures = False):
        """
        overrides the shutdown method to exit the running application and shutdown the touch screen as well
        """

        if self.touch_screen: self.touch_screen.close()
        if self.running_app is not None: self.running_app.terminate()
        if self.running_app is not None: self.running_app.wait(timeout=5)
        super().shutdown(cancel_futures=cancel_futures, wait=wait)
