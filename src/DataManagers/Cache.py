from io import BytesIO
from PIL.Image import open as open_img, new as new_img
from AppData import IMAGE_RESOLUTION
from PIL.ImageDraw import Draw
from shelve import open as open_db

with open_db("AppData/songs") as f, open_db("AppData/albums") as f2:
    for i in f.keys():
        print(i.split("\n")[0])
    print(len(f.keys()) - 1, len(f2.keys()))
    print(f.get("pending queries", set()))


class Cache:
    """
    a class to represent a cache of api queries for album art
    with efficient storage by only storing 1 image per album
    and each song within the album references the same image
    """
    
    # initializes global fields
    image_mask = new_img("L", (IMAGE_RESOLUTION, IMAGE_RESOLUTION), 0)
    Draw(image_mask).rounded_rectangle([0, 0, IMAGE_RESOLUTION, IMAGE_RESOLUTION], radius=10, fill=255)

    def __init__(self, songs_db, albums_db):
        """
        initializes the cache variables

        @param songs_db: the file path to the songs db
        @param albums_db the file path to the albums db
        """

        self.songs_db = songs_db
        self.albums_db = albums_db
        self.songs = None
        self.albums = None
        with open("AppData/default_album_art.png", "rb") as f:
            self.default_art = self.format_bytes(f.read())

    def cache_decorator(self, function):
        """
        a cache decorator function that will automatically open and close the cache before
        and after that function call. This decorator is needed for any function that uses
        the cache to make sure the data is properly read/written

        ** note: cache can become corrupted if pi loses power on one of the close functions
        but the odds of this happening are extremely small so this error will not be considered **

        @param function: the function to decorate
        """

        def wrapper(*args, **kwargs):
            """
            opens the cache, runs the function, closes the cache and returns

            @param args: the args of the function
            @param kwargs: the kwargs of the function
            """

            self.songs = open_db(self.songs_db)
            self.albums = open_db(self.albums_db)
            result = function(*args, **kwargs)
            self.songs.close()
            self.albums.close()
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

        if (album := self.songs.get(f"{title}\n{artist}")) and (image := self.albums.get(album, self.default_art)):
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

        self.songs[f"{title}\n{artist}"] = f"{album}\n{artist.split(',')[0]}"
        if art and (not f"{album}\n{artist.split(',')[0]}" in self.albums):
            self.albums[f"{album}\n{artist.split(',')[0]}"] = self.format_bytes(art)

        return self.albums.get(f"{album}\n{artist.split(',')[0]}") if art else self.default_art
    
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
