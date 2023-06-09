import xbmcaddon
from pathlib import Path
from xbmcvfs import translatePath

import sqlite3 as sql

def create_tables():
    with sql.connect(database()) as conn:
        table = '''
        CREATE TABLE IF NOT EXISTS categories (
            id           TEXT  PRIMARY KEY  NOT NULL,
            expires      INTEGER,
            data         JSON );
        '''
        conn.execute(table)

        table = '''
        CREATE TABLE IF NOT EXISTS favourites (
                id            TEXT  PRIMARY KEY  NOT NULL,
                category      TEXT,
                title         TEXT
                );
        '''
        conn.execute(table)

        table = '''
        CREATE TABLE IF NOT EXISTS mylist (
                id            TEXT  PRIMARY KEY  NOT NULL,
                expires       INTEGER,
                vid_type      TEXT,
                title         TEXT,
                series        TEXT
                );
        '''
        conn.execute(table)


def get_filename():
    addon = xbmcaddon.Addon()
    cache_path = Path(translatePath(addon.getAddonInfo('profile')))
    cache_path.mkdir(parents=True, exist_ok=True)
    fname = str(cache_path/'tver.db')
    return fname

_DB = get_filename()

def database():
    return _DB



