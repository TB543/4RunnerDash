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
    a class to handle jobs that will run in the background
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
        self.obd_lock = Lock()
        self.is_shutdown = False

    def queue_obd_connection_job(self, obd, root):
        """
        queues a job to connect to the obd scanner

        @param obd the obd api instance to connect to the scanner
        @param root the UI element to schedule another connection attempt after a bit of time
        """

        if not self.is_shutdown:
            future = self.submit(lambda: self.obd_connection_job(obd))
            future.add_done_callback(lambda f: self.check_obd_connection(obd, root))

    def obd_connection_job(self, obd):
        """
        attempts to connect to the obd scanner

        @param obd the obd api instance to connect to the scanner
        """

        # lazy loaded for performance
        from obd import Async, commands

        with self.obd_lock:
            try:
                if not obd.is_connected():
                    Async.__init__(obd)
                    obd.watch(commands.MAF)
                    obd.watch(commands.FUEL_LEVEL)
                    obd.watch(commands.SPEED, callback=lambda r: obd.update_loop())
                    obd.start()

            # is_connected can fail
            except:
                    Async.__init__(obd)
                    obd.watch(commands.MAF)
                    obd.watch(commands.FUEL_LEVEL)
                    obd.watch(commands.SPEED, callback=lambda r: obd.update_loop())
                    obd.start()

    def check_obd_connection(self, obd, root):
        """
        checks if obd is connected, if not retry later

        @param obd the obd connection to check
        @param root, the root element to queue the next job with
        """

        # prevents race condition when shutting down
        with self.obd_lock:
            if self.is_shutdown:
                return

            # retries connection on fail
            try:
                if not obd.is_connected():
                    root.after(1000, lambda: self.queue_obd_connection_job(obd, root))
            except:

                # waits until mainloop has started to try connection again
                while True:
                    try:
                        root.after(1000, lambda: self.queue_obd_connection_job(obd, root))
                        return
                    except:
                        pass

    def queue_album_art_job(self, title, artist, album):
        """
        queues an album art job to be completed

        @param title: the title of the track
        @param artist: the artist of the track
        @param album: the album of the track

        @return a future object to access the results of the job when completed
        """

        if not self.is_shutdown:
            future = self.submit(lambda: self.album_art_job(title, artist, album))
            future.add_done_callback(lambda f: self.attempt_query_pending())
            return future

    def album_art_job(self, title, artist, album=None):
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
            self.submit(self.album_art_job, *query)

    def shutdown(self, root, wait = True, *, cancel_futures = False):
        """
        overrides the shutdown method to close the diskcache

        @param root: the UI to update while waiting for jobs to finish to prevent race conditions
        """

        # ensured obd job can finish UI updates
        while not self.obd_lock.acquire():
            root.update()

        # shuts down thread pool and cache
        self.is_shutdown = True
        self.obd_lock.release()
        super().shutdown(cancel_futures=True)
        self.cache.close()
        