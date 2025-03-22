import os
import sys

import xbmc
import xbmcaddon
import xbmcgui

import sqlite3 as sql

from random import randint
from urllib.parse import urlencode

_URL = sys.argv[0]

user_agents = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',

    # Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.5; rv:126.0) Gecko/20100101 Firefox/126.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0',

    # Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',

    # Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
]

def get_url(**kwargs):
    return '{}?{}'.format(_URL, urlencode(kwargs))

def log(msg, level=xbmc.LOGINFO):
    addonID = xbmcaddon.Addon().getAddonInfo('id')
    xbmc.log('%s: %s' % (addonID, msg), level)

def show_info(message):
    xbmcgui.Dialog().notification(localize(30000), message, xbmcgui.NOTIFICATION_INFO, 5000)

def get_random_ua():
    return user_agents[randint(0, len(user_agents) - 1)]

# python embedded (as used in kodi) has a known bug for second calls of strptime. 
# The python bug is docmumented here https://bugs.python.org/issue27400 
# The following workaround patch is borrowed from https://forum.kodi.tv/showthread.php?tid=112916&pid=2914578#pid2914578
def patch_strptime():
    import datetime

    #fix for datatetime.strptime returns None
    class proxydt(datetime.datetime):
        @staticmethod
        def strptime(date_string, format):
            import time
            return datetime.datetime(*(time.strptime(date_string, format)[0:6]))

    datetime.datetime = proxydt

def extract_info(url):
    from lib.yt_dlp import YoutubeDL
    from lib.yt_dlp.extractor.tver import TVerIE

    patch_strptime()

    ydl_opts = {
        'format': 'bestvideo*+bestaudio/best',
        'geo_verification_proxy': get_proxy_url() #or None
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.add_info_extractor(TVerIE()) 
        info = ydl.extract_info(url, download=False)
    return info

def extract_manifest_url_from_info(result):
    if 'manifest_url' in result and get_adaptive_type_from_url(result['manifest_url']):
        return result['manifest_url']

    if 'requested_formats' not in result:
        return None
    
    for entry in result['requested_formats']:
        if 'manifest_url' in entry and 'vcodec' in entry and get_adaptive_type_from_url(entry['manifest_url']):
            return entry['manifest_url']
    return None

def get_adaptive_type_from_url(url):
    supported_endings = [".m3u8", ".hls", ".mpd", ".rtmp", ".ism"]
    file = url.split('/')[-1]
    for ending in supported_endings:
        if ending in file:
            if ending  == ".m3u8":  
                return "hls"
            else:
                return ending.lstrip('.')
    return False

def check_if_kodi_supports_manifest(adaptive_type):
    from inputstreamhelper import Helper
    return Helper(adaptive_type).check_inputstream()

def strip_or_none(v, default=None):
    return v.strip() if isinstance(v, str) else default

def get_addon_path():
    addon = xbmcaddon.Addon()
    return addon.getAddonInfo('path')

def get_proxy_url():
    addon = xbmcaddon.Addon()
    proxy_url = addon.getSetting('proxy_url')
    return strip_or_none(proxy_url)

def get_custom_img_path(file_name):
    return os.path.join(get_addon_path(), 'resources', 'img', file_name)

def lookup_db(db_name):
    from xbmcvfs import translatePath
    database_dir = translatePath("special://database")
    entries = os.listdir(database_dir)
    entries.sort()
    entries.reverse()
    for entry in entries:
        if entry.startswith(db_name) and entry.endswith(".db"):
            return "%s%s" % (database_dir, entry)

    return None

def find_episode(caches, episode_id):
    episode_json = None
    for cache in caches:
        for content in cache['json']['result']['contents']:
            content = content['content']
            if content['id'] == episode_id:
                episode_json = content
                break
    return episode_json

def refresh():
    xbmc.executebuiltin("Container.Refresh")

def localize(string_id):
    return xbmcaddon.Addon().getLocalizedString(string_id)

def clear_thumbnails():
    from xbmcvfs import translatePath, delete
    texturesDb = lookup_db("Textures")
    thumbnailsPath = translatePath("special://thumbnails/")

    conn = sql.connect(texturesDb)
    try:
        with conn:
            textures = conn.execute("SELECT id, cachedurl FROM texture WHERE url LIKE '%%%s%%';" % "statics.tver.jp")
            for texture in textures:
                conn.execute("DELETE FROM sizes WHERE idtexture LIKE '%s';" % texture[0])
                try: 
                    delete( thumbnailsPath + texture[1])
                except: 
                    pass
            conn.execute("DELETE FROM texture WHERE url LIKE '%%%s%%';" % "statics.tver.jp")
    except:
        pass