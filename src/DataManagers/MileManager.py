from json import dump, load
from AppData import MILE_DELTAS
from threading import Lock


class MileManger:
    """
    a class to manage different "trips" to keep track of when
    the car needs oil changes, air filter changes, etc.
    """

    @staticmethod
    def load_key(key, lock=None):
        """
        loads a key from the miles.json file

        @param key: the key to load from the miles.json file
        @param lock: the file lock to use, only passed when getting current miles
            as MileManager cannot be accessed yet

        @return: the value of the key in the miles.json file
        """

        # attempts to load the key from the miles.json file
        lock = lock if lock else MileManger.file_lock
        try:
            with lock:
                with open("AppData/miles.json", "r") as f:
                    return load(f)[key]

        # returns the current miles if an error occurs
        except:
            return MileManger.current_miles + MILE_DELTAS[key] if key in MILE_DELTAS else 0

    # sets global variables shared across all instances of the class
    file_lock = Lock()
    current_miles = load_key("current_miles", file_lock)
    managers = []

    def __init__(self, key, delta, root):
        """
        initializes the MileManager class.

        @param key: the key for the data stored in the miles.json file
        @param delta: a tkinter variable to hold how much longer the fluid/part should last
        @param root: a tkinter widget for scheduling variable updates
        """

        self.key = key
        self.value = self.load_key(self.key)
        self.delta = delta
        self.delta.set(round(self.value - MileManger.current_miles, 2))
        self.root = root
        MileManger.managers.append(self)

    def reset(self):
        """
        calculates when the fluid/part should be replaced and resets the mile counter
        """

        self.value = MileManger.current_miles + MILE_DELTAS[self.key]
        self.root.after(0, lambda: self.delta.set(round(MILE_DELTAS[self.key], 2)))
        MileManger.save()

    @classmethod
    def add_miles(cls, miles):
        """
        adds miles to the current miles and updates all managers.

        @param miles: the number of miles to add to the current miles
        """

        cls.current_miles += miles
        for manager in cls.managers:
            manager.root.after(0, lambda: manager.delta.set(round(manager.value - cls.current_miles, 2)))
        cls.save()

    @classmethod
    def save(cls):
        """
        saves the current miles and all managers to the miles.json file.
        """

        # creates a dictionary to hold the data to be saved
        data = {"current_miles": cls.current_miles}
        for manager in cls.managers:
            data[manager.key] = manager.value

        # writes the data to the miles.json file
        with cls.file_lock:
            with open("AppData/miles.json", "w") as f:
                dump(data, f, indent=4)
