from shelve import open as open_db
from customtkinter import CTkImage
from os import environ
from requests import get, post
from base64 import b64encode
from threading import Timer
from io import BytesIO
from PIL.Image import open as open_img, new as new_img
from PIL.ImageDraw import Draw
from AppData import IMAGE_RESOLUTION


class AlbumArtManager:
    """
    a class to handle management of album art within the music menu
    communicates with spotify API to fetch album art from artists + song name
    caches the art for offline playback
    caches song names that do not have album art when offline for API queries when online
    """

    @staticmethod
    def compress_bytes(bytes):
        """
        compresses an images bytes to the correct resolution

        @param bytes: the bytes to compress
        
        @return the compressed bytes
        """

        image = open_img(BytesIO(bytes)).resize((IMAGE_RESOLUTION, IMAGE_RESOLUTION)).convert("RGBA")
        output = BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()

    # class variables
    token = songs = albums = None
    image_mask = new_img("L", (IMAGE_RESOLUTION, IMAGE_RESOLUTION), 0)
    Draw(image_mask).rounded_rectangle([0, 0, IMAGE_RESOLUTION, IMAGE_RESOLUTION], radius=10, fill=255)
    with open("AppData/default_album_art.png", "rb") as f:
        default_art = compress_bytes(f.read())

    # ======================================== CALLED EXTERNALLY ========================================

    @classmethod
    def get_image(cls, title, artist):
        """
        gets the album art image for the given track
        first the cache is checked
        then an api query is attempted
        if all else fails default image is returned

        @param title: the title of the track
        @param artist: the artist of the track

        @return the image for the track
        """

        # opens database
        with open_db("AppData/songs") as songs, open_db("AppData/albums") as albums:
            cls.songs = songs
            cls.albums = albums

            # handles when no song is playing
            if not (title and artist):
                cls.attempt_query_pending()
                return cls.format_image(cls.default_art)

            # checks if the track is in the cache
            title, artist = title.rsplit(" • ", 1) if " • " in title else (title, artist)
            if (album := songs.get(f"{title}\n{artist}")) and (image := albums.get(album, cls.default_art)):
                cls.attempt_query_pending()
                return cls.format_image(image)

            # attempts to make api query
            if image := cls.request_data(title, artist):
                cls.attempt_query_pending()
                return cls.format_image(image)

            # returns default image 
            pending_queries = songs.get("pending queries", set())
            pending_queries.add((title, artist))
            songs["pending queries"] = pending_queries
            return cls.format_image(cls.default_art)

    # ======================================== CALLED INTERNALLY ========================================

    @classmethod
    def format_image(cls, image):
        """
        formats the image to be used by customtkinter

        @param image: the raw image bytes

        @return a CTkImage with rounded edges
        """

        image = open_img(BytesIO(image))
        image.putalpha(cls.image_mask)
        return CTkImage(light_image=image, dark_image=image, size=(200, 200))

    @classmethod
    def request_token(cls):
        """
        attempts to get an oauth token from spotify for api calls

        @return the token
        """

        # handles when token is already held
        if cls.token:
            return cls.token

        # prepares api call
        credentials = f"{environ['CLIENT_ID']}:{environ['CLIENT_SECRET']}"
        credentials = b64encode(credentials.encode()).decode()

        # sends request
        try:
            response = post(
                "https://accounts.spotify.com/api/token",
                headers={"Authorization": f"Basic {credentials}"},
                data={"grant_type": "client_credentials"},
            ).json()

            # sets token and schedules next call
            cls.token = response["access_token"]
            thread = Timer(response["expires_in"] - 60, lambda: setattr(cls, "token", None))
            thread.daemon = True
            thread.start()
            return cls.token
        except:
            return None

    @classmethod
    def request_data(cls, title, artist):
        """
        attempts to query spotify for the track data

        @return the album name and bytes representing the album art
        """

        # tries various combinations of requests with and without features
        for i, artist_option in enumerate((artist, artist.split(",")[0])):
            for j, title_option in enumerate((title, title.split(" (feat")[0])):
                try:

                    # queries spotify api
                    response = get(
                        "https://api.spotify.com/v1/search", 
                        headers={"Authorization": f"Bearer {cls.request_token()}"}, 
                        params={"q": f'track:"{title_option}" artist:"{artist_option}"', "type": "track", "limit": 1}
                    ).json()

                    # pulls the album name and album art from the response
                    track = response.get("tracks", {}).get("items", [])[0]
                    album_name = track["album"]["name"]
                    album_art = get(track["album"]["images"][0]["url"]).content
                    return cls.cache_data(title, artist, album_name, album_art)
                
                # handles art doesn't exist
                except IndexError:
                    if i == 2 and j == 2:
                        return cls.cache_data(title, artist)
                
                # handles query failures
                except:
                    return

    @classmethod
    def cache_data(cls, title, artist, album=None, art=None):
        """
        caches the results of an api query

        @param title: the title of the song
        @param artist: the artist of the song
        @param album: the album fetched from an api query
        @param art: the art fetched from an api query

        @return the album art
        """

        cls.songs[f"{title}\n{artist}"] = f"{album}\n{artist.split(',')[0]}"
        if art and (not f"{album}\n{artist.split(',')[0]}" in cls.albums):
            cls.albums[f"{album}\n{artist.split(',')[0]}"] = cls.compress_bytes(art)

        return cls.albums[f"{album}\n{artist.split(',')[0]}"] if art else cls.default_art

    @classmethod
    def attempt_query_pending(cls):
        """
        attempts to make api queries for the songs that failed the request_image method
        """

        # iterates over every song
        pending_queries = cls.songs.get("pending queries", set())
        for query in tuple(pending_queries):

            # attempts query and exits if attempt fails
            if cls.request_data(*query):
                pending_queries.remove(query)
            else:
                break

        cls.songs["pending queries"] = pending_queries
