from io import BytesIO
from PIL.Image import open as open_img, new as new_img
from AppData import IMAGE_RESOLUTION, MAX_CACHE_SIZE, MIN_CACHE_SIZE
from PIL.ImageDraw import Draw
from diskcache import Cache
from collections import OrderedDict
from threading import Lock


class AlbumArtCache:
    """
    a class to represent a cache of api queries for album art
    with efficient storage by only storing 1 image per album
    and each song within the album references the same image
    """
    
    # initializes global fields
    image_mask = new_img("L", (IMAGE_RESOLUTION, IMAGE_RESOLUTION), 0)
    Draw(image_mask).rounded_rectangle([0, 0, IMAGE_RESOLUTION, IMAGE_RESOLUTION], radius=10, fill=255)

    def __init__(self, cache_path, default_path):
        """
        initializes the cache variables

        @param path the file path to the image cache
        @param default_path the path to the default image cache
        """

        self.cache = Cache(cache_path)
        self.LRU_lock = Lock()
        self.pending_lock = Lock()
        with open(default_path, "rb") as f:
            self.default_art = self.format_bytes(f.read())

    @classmethod
    def format_bytes(cls, image_bytes):
        """
        compresses an images bytes to the correct resolution and adds rounded corners

        @param bytes: the bytes to format
        
        @return the formatted bytes
        """

        image = open_img(BytesIO(image_bytes)).resize((IMAGE_RESOLUTION, IMAGE_RESOLUTION)).convert("RGBA")
        image.putalpha(cls.image_mask)
        return image
    
    def read_album(self, album):
        """
        marks an album as most recently used (MRU) and reads the data it stores

        @param album the album to read the data of

        @return the album art for the album or the default album art if it does not have any
        """

        # handles no album art
        if not (art := self.cache.get(album)):
            return self.default_art
        
        # marks art album as MRU and returns
        with self.LRU_lock:
            LRU_dict = self.cache.get("LRU", OrderedDict())
            LRU_dict[album] = None
            LRU_dict.move_to_end(album)
            self.cache.set("LRU", LRU_dict)
        return art

    def fetch(self, title, artist):
        """
        attempts to fetch data from the cache 

        @param title: the title of the song
        @param artist: the artist of the song

        @return the cached album art or None if not stored
        """

        if (album := self.cache.get(f"songs:{title}\n{artist}")) and (image := self.read_album(album)):
            return image

    def store_formatted(self, title, artist, album=None, art=None):
        """
        formats and caches the results of an api query

        @param title: the title of the song
        @param artist: the artist of the song
        @param album: the album fetched from an api query
        @param art: the art fetched from an api query

        @return the stored album art (default if not art is given)
        """

        # associates song with album
        key, value = f"{title}\n{artist}", f"albums:{album}\n{artist.split(',')[0]}"
        self.cache.set(f"songs:{key}", value, tag=value)

        # sets album art
        if art and (not value in self.cache):
            self.cache.set(value, self.format_bytes(art), tag=value)
        
        # handles when song has default album art
        elif not art:
            self.cache.set(f"songs:{key}", f"albums:{None}", tag="default")

        # cleans cache if needed and returns
        self.clean()
        return self.read_album(value)
    
    @property
    def pending(self):
        """
        @return after removing the set of all the queries that are pending
        """

        return self.cache.pop("pending", OrderedDict())

    @pending.setter
    def pending(self, value):
        """
        adds to the list of pending queries

        @param value: a pending query
        """

        with self.pending_lock:
            pending = self.cache.get("pending", OrderedDict())
            pending[value] = None
            pending.move_to_end(value)
            self.cache.set(f"pending", pending)

    def clean(self):
        """
        frees up some of the cache by removing elements in order of least recently accessed
        """

        # handles when cache size has not exceeded max
        if self.cache.volume() <= MAX_CACHE_SIZE:
            return

        # removes defaults and pending songs
        with self.LRU_lock, self.cache.transact():
            self.cache.evict(tag="default")
            self.cache.set("pending", set())

            # removes album art in LRU fashion
            LRU = self.cache.get("LRU", OrderedDict())
            while self.cache.volume() >= MIN_CACHE_SIZE and LRU:
                tag, _ = LRU.popitem(last=False)
                self.cache.evict(tag=tag)
            self.cache.set("LRU", LRU)
