from DataManagers.AlbumArtManager import AlbumArtManager
from DataManagers.AppearanceManager import AppearanceManager


# initializes managers
AlbumArtManager.request_token()
AppearanceManager.load()
