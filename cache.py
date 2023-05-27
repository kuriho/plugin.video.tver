import xbmcaddon

import sqlite3 as sql
import json

from pathlib import Path
from xbmcvfs import translatePath
from time import time

def get_filename():
    addon = xbmcaddon.Addon()
    cache_path = Path(translatePath(addon.getAddonInfo('profile')))
    cache_path.mkdir(parents=True, exist_ok=True)
    fname = str(cache_path/'cache.db')
    return fname

class Cache:
    def __init__(self):
        self.file = get_filename()

    def create(self):
        conn = sql.connect(self.file)
        table = '''
        CREATE TABLE IF NOT EXISTS categories (
          id           TEXT  PRIMARY KEY  NOT NULL,
          expires      INTEGER,
          data         JSON );
        '''
        conn.execute(table)
        conn.commit()
        conn.close()

    def get(self, category):
        self.delete_expired()
        conn = sql.connect(self.file)
        cur = conn.cursor()

        data = None

        cur.execute(f'SELECT data FROM categories WHERE id = ?', (category,),)
        results = cur.fetchall()
        if len(results) > 0:
            data = json.loads(results[0][0])   

        cur.close()
        conn.close()

        return data
    
    def get_all(self):
        conn = sql.connect(self.file)
        cur = conn.cursor()

        data = []

        cur.execute(f'SELECT id, data FROM categories')
        results = cur.fetchall()
        for result in results:
            data.append({'id': str(result[0]), 'json': json.loads(result[1])})  

        cur.close()
        conn.close()

        return data


    def insert(self, category, data, expire_after=14400.0):
        conn = sql.connect(self.file)
        #todo: add settings
        expires_at = round(time() + expire_after)
        conn.execute(f'INSERT OR REPLACE INTO categories (id,expires,data) VALUES (?,?,?)', (category, expires_at, json.dumps(data),),)
        conn.commit()
        conn.close()


    def delete_expired(self):
        conn = sql.connect(self.file)
        conn.execute(f'DELETE FROM categories WHERE expires <= ?', (round(time()),),)
        conn.commit()
        conn.close()


    def flush(self):
        conn = sql.connect(self.file)
        conn.execute(f'DELETE FROM categories')
        conn.commit()
        conn.close()