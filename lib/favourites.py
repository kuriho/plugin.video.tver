import sqlite3 as sql
import xbmcgui

from lib.tver import URL_VIDEO_PICTURE
from lib import database, localize

class Favourites:
    def create(self):
        with sql.connect(database()) as conn:
            table = '''
            CREATE TABLE IF NOT EXISTS favourites (
                    id            TEXT  PRIMARY KEY  NOT NULL,
                    category      TEXT,
                    title         TEXT
                    );
            '''
            conn.execute(table)

    def insert(self,category,series,title):
        with sql.connect(database()) as conn:
            conn.execute(f'INSERT OR REPLACE INTO favourites (id,category,title) VALUES (?,?,?)', (series, category, title,),)

    def select(self):
        favs = []

        with sql.connect(database()) as conn:
            cur = conn.execute(f'SELECT id, category, title FROM favourites')
            favs = cur.fetchall()

        return favs

    def delete(self, series):
        with sql.connect(database()) as conn:
            conn.execute(f'DELETE FROM favourites WHERE id = ?', (series,),)

    def list(self):
        series = self.select()
        list = []

        for serie in series:
            li = xbmcgui.ListItem(serie[2])
            list.append(li)

        dialog = xbmcgui.Dialog()
        selected_index = dialog.select(localize(30002), list)
        if selected_index >= 0:
            li = list[selected_index]
            serie = series[selected_index]

            thumb = URL_VIDEO_PICTURE.format('series', serie[0])        
            vid_info = li.getVideoInfoTag()
            vid_info.setTitle(serie[2])
            vid_info.setGenres([serie[1]])
            vid_info.setMediaType('tvshow')

            li.setArt({'thumb': thumb, 'icon': thumb, 'fanart': thumb})
            li.setProperty('IsPlayable', 'false')

            dialog = xbmcgui.Dialog()
            dialog.info(li)