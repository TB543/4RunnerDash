# ignores shutdown when car is off, used for development, best to leave as is
IGNORE_SHUTDOWN = False

# pi screen settings
PI_WIDTH = 1024  # both these might need to be adjusted for pi screen dimensions, hard coded for easier development in other environments
PI_HEIGHT = 600
FPS = 30

# audio playback settings
MAX_VOLUME = 100  # might take some adjusting based on cars sound system
MAX_CACHE_ALBUMS = 90_000  # around 90 gb with 512 resolution, feel free to adjust if needed

# image resolutions
IMAGE_RESOLUTION = 512  # can be adjusted to change the quality of the album art, but will change the size of the image cache
MAP_TILE_RESOLUTION = 256  # changes how big the map tiles are

# default map view when no gps connection
INITIAL_MAP_COORDS = [39.8283, -98.5795]
INITIAL_MAP_ZOOM = 4

# defines how often a fluid/part should be changed where key is the fluid/part and value is how often in miles it should be changed
MILE_DELTAS = {
    "change_oil_at": 5_000,  # for example, this line means oil should be changed every 5000 miles
    "change_filter_at": 15_000,  # to line up with oil change. air filter not oil filter
    "change_transmission_at": 75_000,
}
TANK_CAPACITY = 18.5  # the maximum capacity of your cars gas tank in gallons
