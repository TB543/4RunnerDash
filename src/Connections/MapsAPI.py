class MapsAPI:
    """
    a class to communicate with various mapping services:
        -> GraphHopper connection for routing       port: 8989
        -> TileServer-GL connection for map tiles   port: 8080
        -> Nominatim connection for geocoding       port: 8088
        -> BN-220 GPS module for location           port: /dev/ttyAMA0
    """


def gps():
    import serial

    # Open serial port
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,  # adjust according to your device
        timeout=0  # seconds
    )

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                print(f"Received: {line}")
    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        ser.close()

from threading import Thread
Thread(target=gps, daemon=True).start()
