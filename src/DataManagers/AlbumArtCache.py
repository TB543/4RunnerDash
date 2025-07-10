from AppData import MAX_CACHE_ALBUMS
from diskcache import Cache
from collections import OrderedDict
from threading import Lock


class AlbumArtCache:
    """
    a class to represent a cache of api queries for album art
    with efficient storage by only storing 1 image per album
    and each song within the album references the same image
    """

    def __init__(self, cache_path, default):
        """
        initializes the cache variables

        @param path: the file path to the image cache
        @param default: the default album art to use when none is found
        """

        self.cache = Cache(cache_path)
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
            LRU_dict = self.cache.get("LRU", OrderedDict())

            # ensures song is not added with no matching album
            if not song:
                LRU_dict[album] = None
                LRU_dict.move_to_end(album)
                self.cache.set("LRU", LRU_dict)

            # links song to album if needed
            elif song and (album in LRU_dict):
                self.cache.set(song, album, tag=album)
                LRU_dict[album] = None
                LRU_dict.move_to_end(album)
                self.cache.set("LRU", LRU_dict)
    
    def read_album(self, album, pool, song=None):
        """
        marks an album as most recently used (MRU) and reads the data it stores

        @param album: the album to read the data of
        @param pool: a thread pool owned by the cache manager to handle spawning new jobs if needed
        @param song: the song to link to the album if it is not already

        @return the album art for the album or the default album art if it does not have any
        """
        
        if not (art := self.cache.get(album)):
            return None if song else self.default_art
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
        if (album := self.cache.get(song_key)) and (image := self.read_album(album, pool)):
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
        self.cache.set(key, value, tag=value)

        # sets album art
        if art and (not value in self.cache):
            self.cache.set(value, art, tag=value)
        
        # handles when song has default album art
        elif not art:
            self.cache.set(key, f"albums:{None}", tag="default")

        # removes from pending queries
        with self.pending_lock:
            pending = self.cache.get("pending", OrderedDict())
            pending.pop((title, artist), None)
            self.cache.set(f"pending", pending)

        self.touch_album(value)
        self.clean()
    
    @property
    def pending(self):
        """
        @return after removing the set of all the queries that are pending
        """

        with self.pending_lock:
            return self.cache.get("pending", OrderedDict())

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

    @property
    def token(self):
        """
        gets the api token if it has not expired
        """

        return self.cache.get("token")
    
    @token.setter
    def token(self, value):
        """
        caches the token until it expires

        @param value: the json response from spotify api token request
        """

        self.cache.set("token", value["access_token"], expire=value["expires_in"] - 60)

    def clean(self):
        """
        frees up some of the cache by removing elements in order of least recently accessed
        """

        # gets the LRU
        with self.LRU_lock:
            LRU_dict = self.cache.get("LRU", OrderedDict())

            # removes the least recently accessed album
            while len(LRU_dict) > MAX_CACHE_ALBUMS:
                with self.cache.transact():

                    # removed least recently accessed albums
                    self.cache.evict("default")
                    self.cache.evict(LRU_dict.popitem(last=False)[0])
                    self.cache.set("LRU", LRU_dict)
