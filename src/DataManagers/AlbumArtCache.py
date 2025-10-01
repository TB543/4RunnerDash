from AppData import MAX_CACHE_ALBUMS
from diskcache import Cache
from collections import OrderedDict
from threading import Lock


class AlbumArtCache(Cache):
    """
    a class to represent a cache of api queries for album art
    with efficient storage by only storing 1 image per album
    and each song within the album references the same image
    """

    def __init__(self, default):
        """
        initializes the cache variables

        @param default: the default album art to use when none is found
        """

        super().__init__("AppData/image_cache")
        self.default_art = default
        self.LRU_lock = Lock()
        self.pending_lock = Lock()
    
    def touch_album(self, album, song=None):
        """
        marks an album as most recently used (MRU) and reads the data it stores

        @param album: the album to touch
        @param song: the song to link to the album if it is not already
        """

        with self.LRU_lock:
            LRU_dict = self.get("LRU", OrderedDict())

            # links song to album if needed
            if song and (album in LRU_dict):
                self.set(song, album, tag=album)

            # touches the album
            if (not song) or (song and (album in LRU_dict)):
                LRU_dict[album] = None
                LRU_dict.move_to_end(album)
                self.set("LRU", LRU_dict)
    
    def read_album(self, album, pool, song=None):
        """
        marks an album as most recently used (MRU) and reads the data it stores

        @param album: the album to read the data of
        @param pool: a thread pool owned by the cache manager to handle spawning new jobs if needed
        @param song: the song to link to the album if it is not already

        @return the album art for the album or the default album art if it does not have any
        """
        
        if not (art := self.get(album)):
            return None if song or album != f"albums:{None}" else self.default_art
        pool.submit(self.touch_album, album, song)
        return art
        
    def fetch(self, title, artist, album, pool):
        """
        attempts to fetch data from the cache 

        @param title: the title of the song
        @param artist: the artist of the song
        @param album: the album of the track
        @param pool: a thread pool owned by the cache manager to handle spawning new jobs if needed

        @return the cached album art or None if not stored
        """

        # checks cache with album and artist
        song_key, album_key = f"songs:{title}\n{artist}", f"albums:{album}\n{artist.split(',')[0]}"
        if image := self.read_album(album_key, pool, song_key):
            return image

        # checks cache with song and artist
        if (album := self.get(song_key)) and (image := self.read_album(album, pool)):
            return image

    def store(self, title, artist, album=None, art=None):
        """
        caches the results of an api query

        @param title: the title of the song
        @param artist: the artist of the song
        @param album: the album fetched from an api query
        @param art: the art fetched from an api query
        """

        # associates song with album
        key, value = f"songs:{title}\n{artist}", f"albums:{album}\n{artist.split(',')[0]}"
        self.set(key, value, tag=value)

        # sets album art
        if art and (not value in self):
            self.set(value, art, tag=value)
        
        # handles when song has default album art
        elif not art:
            self.set(key, f"albums:{None}", tag="default")
        self.touch_album(value)

        # removes from pending queries
        with self.pending_lock:
            pending = self.get("pending", OrderedDict())
            pending.pop((title, artist), None)
            self.set(f"pending", pending)

        self.clean()
    
    @property
    def pending(self):
        """
        @return the set of all the queries that are pending
        """

        with self.pending_lock:
            return self.get("pending", OrderedDict())

    @pending.setter
    def pending(self, value):
        """
        adds to the list of pending queries

        @param value: a pending query
        """

        with self.pending_lock:
            pending = self.get("pending", OrderedDict())
            pending[value] = None
            pending.move_to_end(value)
            self.set(f"pending", pending)

    @property
    def token(self):
        """
        gets the api token if it has not expired
        """

        return self.get("token")
    
    @token.setter
    def token(self, value):
        """
        caches the token until it expires

        @param value: the json response from spotify api token request
        """

        self.set("token", value["access_token"], expire=value["expires_in"] - 60)

    def clean(self):
        """
        frees up some of the cache by removing elements in order of least recently accessed
        """

        # gets the LRU
        with self.LRU_lock:
            LRU_dict = self.get("LRU", OrderedDict())

            # removes the least recently accessed album
            while len(LRU_dict) > MAX_CACHE_ALBUMS:
                with self.transact():  # ensures atomicity
                    self.evict("default")
                    self.evict(LRU_dict.popitem(last=False)[0])
                    self.set("LRU", LRU_dict)
