class DHT11:
    """
    a class to represent the DHT11 sensor
    """

    class Result:
        """
        a class to represent the DHT11 sensor readings
        """

        def __init__(self, humidity, temperature):
            """
            initialize the result

            @param humidity: the humidity of the sensor
            @param temperature: the temperature of the sensor
            """

            self.humidity = humidity
            self.temperature = temperature

        @staticmethod
        def is_valid():
            """
            determine if the humidity sensor reading is valid
            always returns True for this dummy library

            @return true
            """

            return True

    def __init__(self, pin):
        """
        initializes the DHT11 with the given pin.

        @param pin: the io pin the dth11 is connected to
        """

    def read(self):
        """
        reads the data from the DHT11 sensor.

        @return: the data
        """

        return DHT11.Result(0, 0)
