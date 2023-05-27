import sys

from utils import lookup_db

import sqlite3 as sql

_URL = sys.argv[0]

class Watcher:
    def __init__(self):
        self.filenameDb = lookup_db("MyVideos")

    def is_watching(self):
        return bool( self.select() )
    
    def select_watched_from_list(self, list):
        if not list:
            return []
        
        watched = []

        conn = sql.connect(self.filenameDb)
        cur = conn.cursor()

        placeholders = ', '.join(['?'] * len(list))

        cur.execute('''
        SELECT strFilename 
            FROM files 
            WHERE     strFilename IN ({}) 
                  AND playCount IS NOT NULL
        '''.format(placeholders), list)

        results = cur.fetchall()

        watched = [result[0] for result in results]

        cur.close()
        conn.close()
        return watched

    def select(self):
        conn = sql.connect(self.filenameDb)
        cur = conn.cursor()

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
        cur.execute(stmt, (_URL,),)

        results = cur.fetchall()

        cur.close()
        conn.close()

        return results