from customtkinter import CTkImage
from Music import SpotifyAPI
from os import environ


class AlbumArt(CTkImage):
    """
    a class to hold and display album art
    """

    api = SpotifyAPI(environ['CLIENT_ID'], environ['CLIENT_SECRET'])
    api.get_album_art(None, None)  # clears pending queries

    def __init__(self, title, artist):
        """
        initializes the image by fetching the album art from the api with the
        title and artist

        @param title: the title of the track
        @param artist: the artist of the track
        """

        image = AlbumArt.api.get_album_art(title, artist)
        super().__init__(image, image, (200, 200))
