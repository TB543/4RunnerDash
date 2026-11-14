from json import load, dump
from datetime import datetime, timedelta


class DateManager:
    """
    a class to manage time based car maintenance
    """

    # loads saved dates
    dates = {}
    maintenance_callback = None  # will be set by parent class
    try:
        with open("AppData/dates.json", "r") as f:
            dates = load(f)
    except:
        pass

    def __init__(self, key, callback):
        """
        initializes the date manager class.

        @param key: the key for the data stored in the dates.json file
        @param callback: the callback function for when the value updates
            ** note: it should take 1 parameter for the new value **
        """

        self.key = key
        self.callback = callback
        if self.key not in DateManager.dates:
            self.value = (datetime.now() + timedelta(days=365)).strftime("%m/%d/%Y")
        self.callback(self.value)

    @property
    def value(self):
        """
        gets the date that this maintenance is needed
        """

        days = self.check_date()
        if days <= 30:
            return f"{days} days"
        return datetime.strptime(DateManager.dates.get(self.key), "%m/%d/%Y").strftime("%m/%d/%y")

    @value.setter
    def value(self, date):
        """
        sets a new date that this maintenance is needed

        :param date: the new date
        """

        DateManager.dates[self.key] = date
        self.callback(self.value)
        self.check_date()
        with open("AppData/dates.json", "w") as f:
            dump(DateManager.dates, f, indent=4)

    def check_date(self):
        """
        checks if the date is less than a month away, notifies the user if so

        :return the number of remaining days
        """

        date = datetime.strptime(DateManager.dates[self.key], "%m/%d/%Y")
        diff = (date - datetime.now()).days
        if diff <= 30:
            DateManager.maintenance_callback()
        return diff
