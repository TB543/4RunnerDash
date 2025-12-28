from json import dump, load
from AppData import MILE_DELTAS


class MileManger:
    """
    a class to manage different "trips" to keep track of when
    the car needs oil changes, air filter changes, etc.
    """

    @staticmethod
    def load_key(key):
        """
        loads a key from the miles.json file

        @param key: the key to load from the miles.json file

        @return: the value of the key in the miles.json file
        """

        # attempts to load the key from the miles.json file
        try:
            with open("AppData/miles.json", "r") as f:
                return load(f)[key]

        # returns the current miles if an error occurs
        except:
            return MileManger.current_miles + MILE_DELTAS[key] if key in MILE_DELTAS else 0

    # sets global variables shared across all instances of the class
    current_miles = load_key("current_miles")
    managers = []

    def __init__(self, key, callback):
        """
        initializes the MileManager class.

        @param key: the key for the data stored in the miles.json file
        @param callback: the callback function for when the value updates
            ** note: it should take 1 parameter for the new value **
        """

        self.key = key
        self.value = self.load_key(self.key)
        self.callback = callback
        MileManger.managers.append(self)
        try:
            self.callback(round(self.value - MileManger.current_miles, 2))
        except:
            return

    def reset(self):
        """
        calculates when the fluid/part should be replaced and resets the mile counter
        """

        self.value = MileManger.current_miles + MILE_DELTAS[self.key]
        try:
            self.callback(round(MILE_DELTAS[self.key], 2))
        except:
            pass

    @classmethod
    def add_miles(cls, miles):
        """
        adds miles to the current miles and updates all managers.

        @param miles: the number of miles to add to the current miles
        """

        cls.current_miles += miles
        for manager in cls.managers:
            try:
                manager.callback(round(manager.value - cls.current_miles, 2))
            except:
                continue

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
        with open("AppData/miles.json", "w") as f:
            dump(data, f, indent=4)
