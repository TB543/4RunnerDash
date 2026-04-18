from json import load, dump


# pi screen settings
PI_WIDTH = 1024  # both these might need to be adjusted for pi screen dimensions, hard coded for easier development in other environments
PI_HEIGHT = 600
FPS = 30  # how often to update music menu

# audio playback settings
MAX_VOLUME = 100  # might take some adjusting based on cars sound system
MAX_CACHED_ALBUMS = 90_000  # around 90 gb with 512 resolution, feel free to adjust if needed

# image resolutions
ALBUM_ART_RESOLUTION = 512  # can be adjusted to change the quality of the album art, but will change the size of the image cache
MAP_TILE_RESOLUTION = 256  # changes how big the map tiles are

# default map view when no gps connection
INITIAL_MAP_COORDS = [39.8283, -98.5795]
INITIAL_MAP_ZOOM = 10

# defines how often a fluid/part should be changed where key is the fluid/part and value is how often in miles it should be changed
MILE_DELTAS = {
    "change_oil_at": 5_000,  # for example, this line means oil should be changed every 5000 miles
    "change_filter_at": 15_000,  # to line up with oil change. air filter not oil filter
    "change_transmission_at": 75_000,
}
TANK_CAPACITY = 18.5  # the maximum capacity of your cars gas tank in gallons

# apps - add as many as you'd like key is app name value is app settings (see example)
APPS = {
    "Shell": None,  # none is default command for exiting this program

    # here is an example app: https://github.com/TB543/4RunnerEffects
    # "4RunnerEffects": { # this program will be hidden but still running in the background while app is running
    #     "command": "~/4RunnerEffects/venv/bin/python ~/4RunnerEffects/src/main.py",  # the command to run the app (required)
    #     "cwd": "~/4RunnerEffects/src",  # working directory of the app (defaults to this programs src directory)
    #     "ignore_shutdown": True,  # determines if app should ignore shutdown when ignition is turned off (defaults to False). behavior will return to normal when program exits
    # } # once the app exits with a return code this program will continue running normally
}

# overrides default settings with saved settings json. note unexpected types will cause unexpected behavior
try:
    with open("AppData/app_settings.json", "r") as f:
        settings = load(f)
        PI_WIDTH = settings["screen"]["width"]
        PI_HEIGHT = settings["screen"]["height"]
        FPS = settings["screen"]["fps"]
        MAX_VOLUME = settings["audio"]["max_volume"]
        MAX_CACHED_ALBUMS = settings["audio"]["max_cached_albums"]
        ALBUM_ART_RESOLUTION = settings["image"]["album_art_resolution"]
        MAP_TILE_RESOLUTION = settings["image"]["map_tile_resolution"]
        INITIAL_MAP_COORDS = settings["map"]["initial_coords"]
        INITIAL_MAP_ZOOM = settings["map"]["initial_zoom"]
        MILE_DELTAS = settings["maintenance"]["mile_deltas"]
        TANK_CAPACITY = settings["maintenance"]["tank_capacity"]
        APPS = settings["apps"]

# writes default settings to json file if an error occurs while reading saved settings
except:
    with open("AppData/app_settings.json", "w") as f:
        settings = {
            "screen": {
                "width": PI_WIDTH,
                "height": PI_HEIGHT,
                "fps": FPS,
            },
            "audio": {
                "max_volume": MAX_VOLUME,
                "max_cached_albums": MAX_CACHED_ALBUMS,
            },
            "image": {
                "album_art_resolution": ALBUM_ART_RESOLUTION,
                "map_tile_resolution": MAP_TILE_RESOLUTION,
            },
            "map": {
                "initial_coords": INITIAL_MAP_COORDS,
                "initial_zoom": INITIAL_MAP_ZOOM,
            },
            "maintenance": {
                "mile_deltas": MILE_DELTAS,
                "tank_capacity": TANK_CAPACITY,
            },
            "apps": APPS,
        }
        dump(settings, f, indent=4)
