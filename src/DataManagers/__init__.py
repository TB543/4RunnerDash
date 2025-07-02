from DataManagers.AlbumArtManager import AlbumArtManager, open_db
from DataManagers.AppearanceManager import AppearanceManager


# initializes managers
AppearanceManager.load()
with open_db("AppData/songs") as songs, open_db("AppData/albums") as albums:
    AlbumArtManager.songs = songs
    AlbumArtManager.albums = albums
    AlbumArtManager.attempt_query_pending()
