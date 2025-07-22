# pi settings
PI_WIDTH = 1024  # both these might need to be adjusted for pi screen dimensions, hard coded for easier development in other environments
PI_HEIGHT = 600

# audio playback settings
MAX_VOLUME = 100  # might take some adjusting based on cars sound system
MAX_CACHE_ALBUMS = 100_000  # less than 70 Gb. I have a lot of extra storage, feel free to adjust if needed
IMAGE_RESOLUTION = 400  # can be adjusted to change the quality of the album art, but will change the size of the image cache

# defines how often a fluid/part should be changed where key is the fluid/part and value is how often in miles it should be changed
MILE_DELTAS = {
    "change_oil_at": 5_000,  # for example, this line means oil should be changed every 5000 miles
    "change_filter_at": 15_000,  # to line up with oil change. air filter not oil filter
    "change_transmission_at": 75_000,
}
TANK_CAPACITY = 18.5  # the maximum capacity of your cars gas tank in gallons
