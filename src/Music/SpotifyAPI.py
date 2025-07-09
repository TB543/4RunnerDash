from DataManagers import AlbumArtCache
from base64 import b64encode
from requests import get, post


class SpotifyAPI:
    """
    a class to handles calls to the Spotify API to get album art
    additionally uses cache for offline calls
    """

    def __init__(self, client_id, client_secret):
        """
        initializes the spotify api

        @param client_id: the client id for the developer app
        @param client_secret: the client secret for the developer app
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.cache = AlbumArtCache("AppData/image_cache", "AppData/default_album_art.png")

    def get_album_art(self, title, artist, album):
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
            self.attempt_query_pending()
            return self.cache.default_art
        
        # checks cache
        split = title.rsplit(" • ")
        title, artist = (split[0], split[-1]) if " • " in title else (title, artist)
        if image := self.cache.fetch(title, artist, album):
            self.attempt_query_pending()
            return image

        # attempts api query
        if image := self.request_data(title, artist):
            self.attempt_query_pending()
            return image
        
        # adds to pending queries and returns default image
        self.cache.pending = (title, artist)
        return self.cache.default_art

    def request_token(self):
        """
        attempts to get an oauth token from spotify for api calls

        @return the token
        """

        # handles when token is already held
        if token := self.cache.token:
            return token

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

            # sets token and returns
            self.cache.token = response
            return response["access_token"]
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
                    return self.cache.store_formatted(title, artist, album_name, album_art)
                
                # handles art doesn't exist
                except IndexError:
                    if i == 2 and j == 2:
                        return self.cache.store_formatted(title, artist)
                
                # handles query failures
                except:
                    return
                
    def attempt_query_pending(self):
        """
        attempts to make api queries for the songs that failed the request_image method
        """

        # iterates over every song
        for query in self.cache.pending:
            self.request_data(*query)
