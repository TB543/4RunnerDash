from io import BytesIO
from PIL.Image import open as open_img, new as new_img
from AppData import IMAGE_RESOLUTION, CACHE_CLEAN_THRESHOLD, CACHE_CLEAN_AMOUNT
from PIL.ImageDraw import Draw
from shelve import open as open_db
from os import remove
from psutil import virtual_memory
from collections import OrderedDict


class AlbumArtCache:
    """
    a class to represent a cache of api queries for album art
    with efficient storage by only storing 1 image per album
    and each song within the album references the same image
    """
    
    # initializes global fields
    image_mask = new_img("L", (IMAGE_RESOLUTION, IMAGE_RESOLUTION), 0)
    Draw(image_mask).rounded_rectangle([0, 0, IMAGE_RESOLUTION, IMAGE_RESOLUTION], radius=10, fill=255)

    def __init__(self):
        """
        initializes the cache variables
        """

        self.songs = None
        self.albums = None
        with open("AppData/default_album_art.png", "rb") as f:
            self.default_art = self.format_bytes(f.read())

    def use(self, function):
        """
        a cache decorator function that will automatically open and close the cache before
        and after that function call. This decorator is needed for any function that uses
        the cache to make sure the data is properly read/written

        ** note: cache can become corrupted if pi loses power on one of the close functions
        but the odds of this happening are extremely small so a backup will not be made,
        instead cache will be cleared in this case **

        @param function: the function to decorate
        """

        def wrapper(*args, **kwargs):
            """
            opens the cache, runs the function, closes the cache and returns

            @param args: the args of the function
            @param kwargs: the kwargs of the function
            """

            # opens cache
            try:
                db = open_db("AppData/album_art_cache")
            except:
                remove("AppData/album_art_cache.db")
                db = open_db("AppData/album_art_cache")


            # sets values and runs function
            self.songs = db.get("songs", {"default": []})
            self.albums = db.get("albums", OrderedDict())
            result = function(*args, **kwargs)

            # stores new values to db and returns
            db["songs"] = self.songs
            db["albums"] = self.albums
            db.close()
            return result

        return wrapper

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

    def fetch_image(self, title, artist):
        """
        attempts to fetch data from the cache 

        @param title: the title of the song
        @param artist: the artist of the song

        @return the cached album art or None if not stored
        """

        if (album := self.songs.get((title, artist))) and (image := self.albums.get(album, {"art": self.default_art})["art"]):
            self.albums.move_to_end(album) if album in self.albums else None
            return image

    def store_formatted_image(self, title, artist, album=None, art=None):
        """
        formats and caches the results of an api query

        @param title: the title of the song
        @param artist: the artist of the song
        @param album: the album fetched from an api query
        @param art: the art fetched from an api query

        @return the stored album art (default if not art is given)
        """

        # stores data
        key, value = (title, artist), (album, artist.split(',')[0])
        self.songs[key] = value
        if art and (not value in self.albums):
            self.albums[value] = {"songs": [key]}
            self.albums[value]["art"] = self.format_bytes(art)
        
        # associates song with album
        elif not art:
            self.songs["default"].append(key)
        else:
            self.albums[value]["songs"].append(key)

        # cleans cache if needed and returns
        self.albums.move_to_end(value) if value in self.albums else None
        self.clean()
        return self.albums.get(value)["art"] if art else self.default_art
    
    @property
    def pending_queries(self):
        """
        gets the set of pending api queries
        """

        return self.songs.get("pending queries", set())

    @pending_queries.setter
    def pending_queries(self, value):
        """
        sets the pending api queries
        """

        self.songs["pending queries"] = value

    def clean(self):
        """
        frees up some of the cache by removing elements in order of least recently accessed
        """

        # checks if clean is needed
        if virtual_memory().percent < CACHE_CLEAN_THRESHOLD:
            return

        # removes the album and any associated songs from the cache
        [self.songs.pop(song) for song in self.songs["default"]]
        for _ in range(int(CACHE_CLEAN_AMOUNT * len(self.albums))):
            for song in self.albums.popitem(last=False)[1]["songs"]:
                self.songs.pop(song)
        