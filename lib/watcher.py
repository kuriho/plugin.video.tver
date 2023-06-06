import sys
import sqlite3 as sql

from urllib.parse import parse_qsl
from lib import Cache, lookup_db, find_episode, strip_or_none, URL_VIDEO_PICTURE

_URL = sys.argv[0]
_DB = lookup_db("MyVideos")

class Watcher:
    def is_watching(self):
        return bool( self.select() )
    
    def select(self):
        results = []

        with sql.connect(_DB) as conn:
            stmt = '''
            SELECT f.strFilename,
                b.timeInSeconds,
                b.totalTimeInSeconds
                FROM bookmark as b
                    INNER JOIN files as f ON f.idFile = b.idFile
                    INNER JOIN path as p ON p.idPath = f.idPath
                WHERE     f.playCount IS NULL
                    AND p.strPath = ?
            '''
            cur = conn.execute(stmt, (_URL,),)
            results = cur.fetchall()

        return results
    
    def select_watched_from_list(self, list):
        if not list:
            return []
        
        placeholders = ', '.join(['?'] * len(list))
        watched = []

        with sql.connect(_DB) as conn:
            cur = conn.execute('''
            SELECT strFilename 
                FROM files 
                WHERE     strFilename IN ({}) 
                    AND playCount IS NOT NULL
            '''.format(placeholders), list)
            results = cur.fetchall()

        watched = [result[0] for result in results]

        return watched
    
    def get_watching_episodes(self):
        episodes = []

        watching = Watcher().select()

        if watching:
            caches = Cache().get_all()

            for row in watching:
                file = row[0]
                params = dict(parse_qsl(file))
                tver_url = params['video']
                video_id = str(tver_url).split('/')[-1]

                #in case the video was pulled from TVer
                label = video_id

                episode = find_episode(caches, video_id)
                if episode:
                    label = ' '.join(filter(None, [strip_or_none(episode['seriesTitle']), strip_or_none(episode['title'])]))

                episodes.append({ 'name': label,
                                'series': None, 
                                'thumb': URL_VIDEO_PICTURE.format('episode', video_id),
                                'video': tver_url, 
                                'genre': None })    

        return episodes