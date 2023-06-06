import sqlite3 as sql
import json

from time import time
from lib import database

class Cache:
    def create(self):
        with sql.connect(database()) as conn:
            table = '''
            CREATE TABLE IF NOT EXISTS categories (
                id           TEXT  PRIMARY KEY  NOT NULL,
                expires      INTEGER,
                data         JSON );
            '''
            conn.execute(table)

    def get(self, category):
        data = None
        self.delete_expired()

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