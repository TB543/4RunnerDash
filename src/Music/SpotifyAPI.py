from DataManagers import AlbumArtCache
from base64 import b64encode
from requests import get, post
from threading import Timer


class SpotifyAPI:
    """
    a class to handles calls to the Spotify API to get album art
    additionally uses cache for offline calls
    """

    cache = AlbumArtCache()

    def __init__(self, client_id, client_secret):
        """
        initializes the spotify api

        @param client_id: the client id for the developer app
        @param client_secret: the client secret for the developer app
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    @cache.cache_decorator
    def get_album_art(self, title, artist):
        """
        attempts to retrieve the data in the following order:
            -> checks cache
            -> attempts api call
            -> default image

        @param title: the title of the track
        @param artist: the artist of the track

        @return image representing the album art
        """
        
        # handles when no song is playing
        if not (title and artist):
            self.attempt_query_pending()
            return SpotifyAPI.cache.default_art
        
        # checks cache
        split = title.rsplit(" • ")
        title, artist = (split[0], split[-1]) if " • " in title else (title, artist)
        if image := SpotifyAPI.cache.fetch_image(title, artist):
            self.attempt_query_pending()
            return image

        # attempts api query
        if image := self.request_data(title, artist):
            self.attempt_query_pending()
            return image
        
        # adds to pending queries and returns default image
        pending = SpotifyAPI.cache.pending_queries
        pending.add((title, artist))
        SpotifyAPI.cache.pending_queries = pending
        return SpotifyAPI.cache.default_art

    def request_token(self):
        """
        attempts to get an oauth token from spotify for api calls

        @return the token
        """

        # handles when token is already held
        if self.token:
            return self.token

        # prepares api call
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials = b64encode(credentials.encode()).decode()

        # sends request
        try:
            response = post(
                "https://accounts.spotify.com/api/token",
                headers={"Authorization": f"Basic {credentials}"},
                data={"grant_type": "client_credentials"},
            ).json()

            # sets token and schedules next call
            self.token = response["access_token"]
            thread = Timer(response["expires_in"] - 60, lambda: setattr(self, "token", None))
            thread.daemon = True
            thread.start()
            return self.token
        except:
            return None

    def request_data(self, title, artist):
        """
        attempts to query spotify for the track data

        @param title: the title of the track
        @param artist: the artist of the track

        @return bytes representing the album art or None if the query fails
        """

        # tries various combinations of requests with and without features
        for i, artist_option in enumerate((artist, artist.split(",")[0])):
            for j, title_option in enumerate((title, title.split(" (feat")[0])):
                try:

                    # queries spotify api
                    response = get(
                        "https://api.spotify.com/v1/search", 
                        headers={"Authorization": f"Bearer {self.request_token()}"}, 
                        params={"q": f'track:"{title_option}" artist:"{artist_option}"', "type": "track", "limit": 1}
                    ).json()

                    # pulls the album name and album art from the response
                    track = response.get("tracks", {}).get("items", [])[0]
                    album_name = track["album"]["name"]
                    album_art = get(track["album"]["images"][0]["url"]).content
                    return SpotifyAPI.cache.store_formatted_image(title, artist, album_name, album_art)
                
                # handles art doesn't exist
                except IndexError:
                    if i == 2 and j == 2:
                        return SpotifyAPI.cache.store_formatted_image(title, artist)
                
                # handles query failures
                except:
                    return
                
    def attempt_query_pending(self):
        """
        attempts to make api queries for the songs that failed the request_image method
        """

        # iterates over every song
        pending = SpotifyAPI.cache.pending_queries
        for query in tuple(pending):

            # attempts query and exits if attempt fails
            if self.request_data(*query):
                pending.remove(query)
            else:
                break

        SpotifyAPI.cache.pending_queries = pending
