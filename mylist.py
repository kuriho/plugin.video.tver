import sys
import sqlite3 as sql

from time import time
from cache import Cache, get_filename
from tver import URL_VIDEO_PICTURE, URL_VIDEO_WEBSITE
from watcher import Watcher
from utils import strip_or_none, get_url
from urllib.parse import parse_qsl

_URL = sys.argv[0]

class MyList:
    def __init__(self):
        self.file = get_filename()

    def create(self):
        conn = sql.connect(self.file)
        table = '''
        CREATE TABLE IF NOT EXISTS mylist (
                id            TEXT  PRIMARY KEY  NOT NULL,
                expires       INTEGER,
                vid_type      TEXT,
                title         TEXT,
                series        TEXT,
                series_title  TEXT
                );
        '''
        conn.execute(table)
        conn.commit()

        table = '''
        CREATE TABLE IF NOT EXISTS favourites (
                id            TEXT  PRIMARY KEY  NOT NULL,
                category      TEXT
                );
        '''
        conn.execute(table)
        conn.commit()
        conn.close()

    def build(self):
        mylist = [item[0] for item in self.select()]

        favourites = self.select_favourites()
        categories = list(set([fav[1] for fav in favourites]))
        series = [fav[0] for fav in favourites]

        for category in categories:
            cached_episodes = Cache().get(category)

            for episode in cached_episodes['result']['contents']:
                series_id = episode['content']['seriesID']
                if series_id in series:
                    video_id = episode['content']['id']
                    if video_id in mylist:
                        continue
                    self.insert(episode['type'],episode['content'])
                    

    def add(self,category,series):
        conn = sql.connect(self.file)
        conn.execute(f'INSERT OR REPLACE INTO favourites (id,category) VALUES (?,?)', (series, category,),)
        conn.commit()
        conn.close()
        #rebuild mylist
        self.build()

    def remove(self,series):
        conn = sql.connect(self.file)
        conn.execute(f'DELETE FROM favourites WHERE id = ?', (series,),)
        conn.commit()
        conn.execute(f'DELETE FROM mylist WHERE series = ?', (series,),)
        conn.commit()
        conn.close()

    def select_favourites(self):
        conn = sql.connect(self.file)
        cur = conn.cursor()

        stmt = '''
        SELECT id,
               category
            FROM favourites
        '''
        cur.execute(stmt)

        favs = cur.fetchall()

        cur.close()
        conn.close()

        return favs

    def select(self):
        conn = sql.connect(self.file)
        cur = conn.cursor()

        stmt = '''
        SELECT id,
               vid_type,
               title,
               series,
               series_title 
            FROM mylist
        '''
        cur.execute(stmt)

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results
    
    def insert(self, type, content):
        conn = sql.connect(self.file)

        conn.execute('''
        INSERT OR REPLACE INTO mylist (id,expires,vid_type,title,series,series_title) 
            VALUES (?,?,?,?,?,?)
        ''', 
        (content['id'], content['endAt'], type, content['title'], content['seriesID'], content['seriesTitle'],),)

        conn.commit()
        conn.close()

    def get(self):
        self.delete_expired()
        mylist = self.select()
        #todo: add settings
        watched = [str(dict(parse_qsl(entry))['video']).split('/')[-1] for entry in Watcher().select_watched_from_list([get_url(action='play', video=URL_VIDEO_WEBSITE.format(item[1], item[0])) for item in mylist])]

        episodes = []

        for (video_id, video_type, title, series_id, series_title) in mylist:
            if video_id in watched:
                continue
            label = ' '.join(filter(None, [strip_or_none(series_title), strip_or_none(title)]))
            episodes.append({ 'name': label,
                              'series': series_id, 
                              'thumb': URL_VIDEO_PICTURE.format(video_type, video_id),
                              'video': URL_VIDEO_WEBSITE.format(video_type, video_id), 
                              'genre': None })

        return episodes
    
    def get_random_pic(self):
        pic = None

        conn = sql.connect(self.file)
        cur = conn.cursor()

        stmt = f'SELECT id, vid_type FROM mylist ORDER BY RANDOM() LIMIT 1'
        cur.execute(stmt)

        results = cur.fetchall()

        cur.close()
        conn.close()
        if results:
            pic = URL_VIDEO_PICTURE.format(results[0][1], results[0][0])

        return pic

    def delete_expired(self):
        conn = sql.connect(self.file)
        conn.execute(f'DELETE FROM mylist WHERE expires <= ?', (round(time()),),)
        conn.commit()
        conn.close()

    def flush(self):
        conn = sql.connect(self.file)
        conn.execute(f'DELETE FROM mylist')
        conn.commit()
        conn.close()