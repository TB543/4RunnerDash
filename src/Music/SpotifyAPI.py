from base64 import b64encode
from requests import get, post


class SpotifyAPI:
    """
    a class to handles calls to the Spotify API to get album art
    """

    def __init__(self, client_id, client_secret):
        """
        initializes the spotify api

        @param client_id: the client id for the developer app
        @param client_secret: the client secret for the developer app
        """

        self.client_id = client_id
        self.client_secret = client_secret

    def request_token(self):
        """
        attempts to get an oauth token from spotify for api calls

        @return the token
        """

        # prepares api call
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials = b64encode(credentials.encode()).decode()

        # sends request
        try:
            response = post(
                "https://accounts.spotify.com/api/token",
                headers={"Authorization": f"Basic {credentials}"},
                data={"grant_type": "client_credentials"},
                timeout=5
            ).json()

            # sets token and returns
            return response
        except:
            return {"access_token": None, "expires_in": 0}

    @staticmethod
    def request_data(title, artist, token):
        """
        attempts to query spotify for the track data

        @param title: the title of the track
        @param artist: the artist of the track
        @param token: the api token

        @return a list containing the track data: [title, artist, album, art]
        """

        # tries various combinations of requests with and without features
        for i, artist_option in enumerate((artist, artist.split(",")[0])):
            for j, title_option in enumerate((title, title.split(" (feat")[0])):
                try:

                    # queries spotify api
                    response = get(
                        "https://api.spotify.com/v1/search", 
                        headers={"Authorization": f"Bearer {token}"}, 
                        params={"q": f'track:"{title_option}" artist:"{artist_option}"', "type": "track", "limit": 1},
                        timeout=5
                    ).json()

                    # pulls the album name and album art from the response
                    track = response.get("tracks", {}).get("items", [])[0]
                    album_name = track["album"]["name"]
                    album_art = get(track["album"]["images"][0]["url"], timeout=5).content
                    return [title, artist, album_name, album_art]
                
                # handles art doesn't exist
                except IndexError:
                    if i == 2 and j == 2:
                        return [title, artist]
                
                # handles query failures
                except:
                    return
