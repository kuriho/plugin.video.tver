import sqlite3 as sql
import json

from time import time

from lib.tver import fetch_episodes, URL_VIDEO_PICTURE, URL_VIDEO_WEBSITE
from lib import database, strip_or_none


class Cache:
    def get(self, category):
        data = None

        with sql.connect(database()) as conn:
            cur = conn.execute(f'SELECT data FROM categories WHERE id = ?', (category,),)
            results = cur.fetchall()

        if len(results) > 0:
            data = json.loads(results[0][0])   

        return data
    
    def get_all(self):
        data = []
        
        with sql.connect(database()) as conn:
            cur = conn.execute(f'SELECT id, data FROM categories')
            results = cur.fetchall()

        for result in results:
            data.append({'id': str(result[0]), 'json': json.loads(result[1])})  

        return data

    def insert(self, category, data, expire_after=14400.0):
        expires_at = round(time() + expire_after)
        
        with sql.connect(database()) as conn:
            conn.execute(f'INSERT OR REPLACE INTO categories (id,expires,data) VALUES (?,?,?)', (category, expires_at, json.dumps(data),),)


    def delete_expired(self):
        with sql.connect(database()) as conn:
            conn.execute(f'DELETE FROM categories WHERE expires <= ?', (round(time()),),)

    def get_or_download(self, category):
        json_episodes = self.get(category)
        if not json_episodes:
            json_episodes = fetch_episodes(category)
            self.insert(category, json_episodes)
        return json_episodes

    def get_episodes(self, category):
        json_episodes = self.get_or_download(category)
            
        episodes = []

        for episode in json_episodes['result']['contents']:
            video_type = episode['type']
            
            if video_type == 'episode':
                series_id = episode['content']['seriesID']
                video_id = episode['content']['id']
                series_title = strip_or_none(episode['content']['seriesTitle'])
                label = ' '.join(filter(None, [series_title, strip_or_none(episode['content']['title'])]))
                episodes.append({ 'name': label,
                                'series': series_id, 
                                'thumb': URL_VIDEO_PICTURE.format(video_type, video_id),
                                'video': URL_VIDEO_WEBSITE.format(video_type, video_id), 
                                'genre': category, 
                                'series_title': series_title })

        return episodes
