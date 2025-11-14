from concurrent.futures import ThreadPoolExecutor
from DataManagers.AlbumArtCache import AlbumArtCache
from Connections.SpotifyAPI import SpotifyAPI
from io import BytesIO
from PIL.Image import open as open_img, new as new_img
from AppData import IMAGE_RESOLUTION
from PIL.ImageDraw import Draw
from threading import Lock


class BGJobManager(ThreadPoolExecutor):
    """
    a class to handle background api request threads
    """

    # initializes global fields
    image_mask = new_img("L", (IMAGE_RESOLUTION, IMAGE_RESOLUTION), 0)
    Draw(image_mask).rounded_rectangle([0, 0, IMAGE_RESOLUTION, IMAGE_RESOLUTION], radius=12, fill=255)

    def __init__(self):
        """
        initializes the request manager and its fields
        """

        super().__init__()
        with open("AppData/default_album_art.png", "rb") as f:
            self.default_art = self.format_bytes(f.read())

        self.api = SpotifyAPI()
        self.cache = AlbumArtCache(self.default_art)
        self.token_lock = Lock()

    def queue_job(self, title, artist, album):
        """
        queues a job to be completed

        @param title: the title of the track
        @param artist: the artist of the track
        @param album: the album of the track

        @return a future object to access the results of the job when completed
        """

        future = self.submit(lambda: self.job(title, artist, album))
        future.add_done_callback(lambda f: self.attempt_query_pending())
        return future

    def job(self, title, artist, album=None):
        """
        attempts to retrieve the data in the following order:
            -> checks cache
            -> attempts api call
            -> default image

        @param title: the title of the track
        @param artist: the artist of the track
        @param album: the album of the track

        @return image representing the album art
        """

        # handles when no song is playing
        if not (title and artist):
            return self.default_art
        
        # handles songs with no artists
        split = title.rsplit(" • ")
        title, artist = (split[0], split[-1]) if " • " in title else (title, artist)
        if not artist:
            return self.default_art

        # checks cache
        if image := self.cache.fetch(title, artist, album, self):
            return image

        # attempts api query
        if data := self.api.request_data(title, artist, self.get_token()):
            image = self.default_art
            if len(data) == 4:
                data[3] = image = self.format_bytes(data[3])

            # queues cache store and returns
            self.submit(self.cache.store, *data)
            return image
        
        # adds to pending queries and returns default image
        self.cache.pending = (title, artist)
        return self.default_art
    
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
    
    def get_token(self):
        """
        attempts to get the token in the following order
            -> checks cache
            -> attempts api call

        @return the token if it is found
        """

        # cache hit
        with self.token_lock:
            if token := self.cache.token:
                return token
            
            # token expired
            token = self.api.request_token()
            self.cache.token = token
            return token["access_token"]
    
    def attempt_query_pending(self):
        """
        attempts to make api queries for the songs that failed the request_image method
        """

        # iterates over every song
        for query in self.cache.pending:
            self.submit(self.job, *query)

    def shutdown(self, wait = True, *, cancel_futures = False):
        """
        overrides the shutdown method to close the diskcache
        """

        super().shutdown(cancel_futures=True)
        self.cache.close()
        