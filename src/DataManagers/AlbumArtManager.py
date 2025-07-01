from shelve import open as open_db
from requests import get, post
from base64 import b64encode
from threading import Timer


class AlbumArtManager:
    """
    a class to handle management of album art within the music menu
    communicates with spotify API to fetch album art from artists + song name
    caches the art for offline playback
    caches song names that do not have album art when offline for API queries when online
    """

    token = None  # will be set when given by spotify api

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

        # checks if the track is in the cache
        with open_db("AppData/songs") as songs, open_db("AppData/albums") as albums:
            if (album := songs.get(f"{title}\n{artist}")) and (image := albums.get(album)):
                return image

        # attempts to make api query todo
        return cls.request_data(title, artist)[1]

        # returns default image 
        with opendb("AppData/songs") as songs:
            pending_queries = songs.get("pending queries", [])
            pending_queries.append(f"{title}\n{artist}")
            songs["pending queries"] = pending_queries
        return None  # todo default image

    # ======================================== CALLED INTERNALLY ========================================

    @classmethod
    def request_token(cls):
        """
        attempts to get an oauth token from spotify for api calls
        """

        client_id = ""
        client_secret = ""

        # prepares api call
        credentials = f"{client_id}:{client_secret}"
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
            thread = Timer(response["expires_in"] - 10, cls.request_token)
            cls.attempt_query_pending()
        except:
            thread = Timer(30, cls.request_token)
        thread.daemon = True
        thread.start()

    @classmethod
    def attempt_query_pending(cls):
        """
        attempts to make api queries for the songs that failed the request_image method
        """

        # iterates over every song
        with open_db("AppData/songs") as songs:
            pending_queries = songs.get("pending queries", [])
            while pending_queries:

                # attempts query and exits if attempt fails
                try:
                    song = pending_queries[-1]  # todo query
                    pending_queries.pop()
                except:
                    break
            
            songs["pending queries"] = pending_queries

    @classmethod
    def request_data(cls, title, artist):
        """
        attempts to query spotify for the track data

        @throws error if request fails: times out, no internet, bad request, etc

        @return the album name and album art
        """

        # queries spotify api
        response = get(
            "https://api.spotify.com/v1/search", 
            headers={"Authorization": f"Bearer {cls.token}"}, 
            params={"q": f'track:"{title}" artist:"{artist}"', "type": "track", "limit": 1}
        ).json()

        # pulls the album name and album art from the response
        track = response.get("tracks", {}).get("items", [])[0]
        album_name = track["album"]["name"]
        art_length = len(track["album"]["images"])
        album_art = get(track["album"]["images"][(5 * art_length) // 8]["url"]).content
        return album_name, album_art
