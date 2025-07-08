# constants for pi settings
PI_WIDTH = 1024
PI_HEIGHT = 600
MAX_VOLUME = 100
MAX_CACHE_SIZE = 5_368_709_120  # 5 gb in bytes
MIN_CACHE_SIZE = 4_294_967_296  # albums will be removed until this value (4 gb) is met if max size is exceeded

# default fonts and resolution
MENU_ICON_FONT = ("Arial", 100)
MENU_LABEL_FONT = ("Arial", 20)
IMAGE_RESOLUTION = 400

# widgets settings
SONG_TITLE_LABEL_KWARGS = {"height": 15, "font": ("Arial", 12, "bold"), "anchor": "w"}
SONG_ARTIST_LABEL_KWARGS = {"height": 10, "font": ("Arial", 10), "anchor": "w"}
SONG_TIME_LABEL_KWARGS = {"height": 8, "font": ("Arial", 8)}
TRACK_CONTROL_BUTTON_KWARGS = {"width": 75, "height": 35, "font": ("Arial", 15), "corner_radius": float("inf")}
TRACK_SEEK_BUTTON_KWARGS = {"width": 50, "height": 20, "font": ("Arial", 10), "corner_radius": float("inf")}
VOLUME_BUTTON_KWARGS = {"width": 17, "height": 15, "font": ("Arial", 15), "corner_radius": float("inf")}
