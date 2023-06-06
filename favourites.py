import xbmcgui

from mylist import MyList

def show_favourites():
    series = MyList().select_favourites()
    list = []

    for serie in series:
        li = xbmcgui.ListItem(serie[2])
        list.append(li)

    dialog = xbmcgui.Dialog()
    selected_index = dialog.select("MyList", list)
    if selected_index >= 0:
        li = list[selected_index]
        serie = series[selected_index]

        thumb = 'https://statics.tver.jp/images/content/thumbnail/series/small/{}.jpg'.format(serie[0])        
        vid_info = li.getVideoInfoTag()
        vid_info.setTitle(serie[2])
        vid_info.setGenres([serie[1]])
        vid_info.setMediaType('tvshow')

        li.setArt({'thumb': thumb, 'icon': thumb, 'fanart': thumb})
        li.setProperty('IsPlayable', 'false')

        dialog = xbmcgui.Dialog()
        dialog.info(li)