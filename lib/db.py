import xbmcaddon
from pathlib import Path
from xbmcvfs import translatePath

def get_filename():
    addon = xbmcaddon.Addon()
    cache_path = Path(translatePath(addon.getAddonInfo('profile')))
    cache_path.mkdir(parents=True, exist_ok=True)
    fname = str(cache_path/'tver.db')
    return fname

_DB = get_filename()

def database():
    return _DB



