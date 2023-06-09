import sqlite3 as sql

from time import time

from lib.tver import URL_VIDEO_PICTURE, URL_VIDEO_WEBSITE
from lib import Cache, Watcher, Favourites, strip_or_none, get_url, database

from urllib.parse import parse_qsl

class MyList:
    def __init__(self):
        self.favourites = Favourites()
        
    def build(self):
        mylist = [item[0] for item in self.select()]
        favourites = self.favourites.select()

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
                    

    def add(self,category,series,title):
        self.favourites.insert(category,series,title)
        self.build()

    def remove(self,series):
        self.favourites.delete(series)
        self.delete(series)

    def get(self):
        self.delete_expired()
        mylist = self.select()

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
                              'genre': None,
                              'series_title': series_title })

        return episodes
    
    def get_random_pic(self):
        pic = None

        with sql.connect(database()) as conn:
            stmt = f'SELECT id, vid_type FROM mylist ORDER BY RANDOM() LIMIT 1'
            cur = conn.execute(stmt)
            results = cur.fetchall()

        if results:
            pic = URL_VIDEO_PICTURE.format(results[0][1], results[0][0])

        return pic
    
    def select(self):
        results = []

        with sql.connect(database()) as conn:
            stmt = '''
            SELECT my.id,
                my.vid_type,
                my.title,
                fav.id as series,
                fav.title as series_title 
                FROM mylist as my 
                INNER JOIN favourites as fav on fav.id = my.series
            '''
            cur = conn.execute(stmt)
            results = cur.fetchall()

        return results
    
    def insert(self, type, content):
        with sql.connect(database()) as conn:
            conn.execute('''
            INSERT OR REPLACE INTO mylist (id,expires,vid_type,title,series) 
                VALUES (?,?,?,?,?)
            ''', 
            (content['id'], content['endAt'], type, content['title'], content['seriesID'], ),)

    def delete(self, series):
        with sql.connect(database()) as conn:
            conn.execute(f'DELETE FROM mylist WHERE series = ?', (series,),)

    def delete_expired(self):
        with sql.connect(database()) as conn:
            conn.execute(f'DELETE FROM mylist WHERE expires <= ?', (round(time()),),)