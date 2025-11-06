from base64 import b64encode
from os import environ


class SpotifyAPI:
    """
    a class to handles calls to the Spotify API to get album art
    """

    TOKEN_URL = "https://accounts.spotify.com/api/token"
    SEARCH_URL = "https://api.spotify.com/v1/search"

    def __init__(self):
        """
        initializes the spotify api
        """

        self.client_id = environ['CLIENT_ID']
        self.client_secret = environ['CLIENT_SECRET']

    def request_token(self):
        """
        attempts to get an oauth token from spotify for api calls

        @return the token
        """

        # prepares api call
        from requests import post  # lazy loaded for performance
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials = b64encode(credentials.encode()).decode()

        # sends request
        try:
            response = post(
                SpotifyAPI.TOKEN_URL,
                headers={"Authorization": f"Basic {credentials}"},
                data={"grant_type": "client_credentials"},
                timeout=5
            ).json()

            # sets token and returns
            return response
        except:
            return {"access_token": None, "expires_in": 0}

    @classmethod
    def request_data(cls, title, artist, token):
        """
        attempts to query spotify for the track data

        @param title: the title of the track
        @param artist: the artist of the track
        @param token: the api token

        @return a list containing the track data: [title, artist, album, art]
        """

        # tries various combinations of requests with and without features
        from requests import get  # lazy loaded for performance
        for i, artist_option in enumerate((artist, artist.split(",")[0])):
            for j, title_option in enumerate((title, title.split(" (feat")[0])):
                try:

                    # queries spotify api
                    response = get(
                        cls.SEARCH_URL,
                        headers={"Authorization": f"Bearer {token}"}, 
                        params={"q": f'track:"{title_option}" artist:"{artist_option}"', "type": "track", "limit": 1},
                        timeout=5
                    ).json()

                    # pulls the album name and album art from the response
                    track = response.get("tracks", {}).get("items", [])[0]
                    album_name = track["album"]["name"]
                    album_art = get(track["album"]["images"][0]["url"]).content
                    return [title, artist, album_name, album_art]
                
                # handles art doesn't exist
                except IndexError:
                    if i == 2 and j == 2:
                        return [title, artist]
                
                # handles query failures
                except:
                    return
