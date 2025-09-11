from concurrent.futures import ThreadPoolExecutor
from time import time
try:
    from evdev.ecodes import BTN_TOUCH
except ModuleNotFoundError:
    from Dev.Imports.evdev import *


class FGJobManager:
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

        self.pool = ThreadPoolExecutor()
        self.touch_screen = touch_screen

    def queue_display_sleep(self, wake):
        """
        creates a display sleep job. ie wait for input to wake up the display

        @param wake: the function to call to wake up the display when an input is given
        """

        future = self.pool.submit(self.display_sleep_job)
        future.add_done_callback(lambda f: wake())

    def queue_address_search(self, address, done):
        """
        creates an address search job

        @param address: the address to search
        @param done: the callback function to call when the address search is done

        @return: a future object for accessing the coordinates of the address
        """

    def queue_routing(self, destination, done):
        """
        creates a routing job

        @param destination: the coordinates of the destination
        @param done: the callback function to call when the routing is done

        @return: a future object for accessing the calculated route later
        """

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

    def address_search_job(self, address):
        """
        the job for address search, queries the navigation api and waits for the response

        @param address: the address to search

        @return: the response from the navigation api containing the coordinates of the address
        """

    def routing_job(self, destination):
        """
        the job for routing, queries the navigation api and waits for the response

        @param destination: the coordinates of the destination

        @return: the response from the navigation api containing the route to the destination
        """

    def shutdown(self):
        """
        shuts down the thread pool when it is no longer needed
        """

        self.pool.shutdown(cancel_futures=True)
