import sys
from urllib.parse import parse_qsl
import xbmcgui
import xbmcplugin

from lib import tver
from lib import Cache, Favourites, Watcher, MyList

from lib import log, show_info, check_if_kodi_supports_manifest, extract_info, extract_manifest_url_from_info, get_url, refresh, get_adaptive_type_from_url, localize, clear_thumbnails

_HANDLE = int(sys.argv[1])

def list_videos(category):
    xbmcplugin.setPluginCategory(_HANDLE, category)
    xbmcplugin.setContent(_HANDLE, 'videos')

    videos = []
    context = None

    if category == 'mylist':
        mylist = MyList()
        mylist.build()
        videos = mylist.get()
        context = (localize(30020),'delist')

    elif category == 'watching':
        videos = Watcher().get_watching_episodes()

    else:
        videos = Cache().get_episodes(category)
        context = (localize(30021),'mylist')

    for video in videos:
        label = video['name']

        list_item = xbmcgui.ListItem(label=label, offscreen=True)
        
        vid_info = list_item.getVideoInfoTag()
        vid_info.setTitle(label)
        vid_info.setGenres([video['genre']])
        vid_info.setTvShowTitle(video['series'])
        vid_info.setMediaType('video')

        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')

        if context:
            context_menu_item = (context[0], 'RunPlugin({})'.format(get_url(action=context[1], series=video['series'], category=video['genre'], series_title=video['series_title'])))
            list_item.addContextMenuItems([context_menu_item])

        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    
    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_HANDLE)

def get_categories():
    cats = tver.get_categories()

    if Watcher().is_watching():
        cats.insert(0,("watching", localize(30003), None))

    mylist_pic = MyList().get_random_pic()
    if mylist_pic:
        cats.insert(0,("mylist", localize(30002), mylist_pic))

    return cats

def list_categories():
    xbmcplugin.setPluginCategory(_HANDLE, '...')
    xbmcplugin.setContent(_HANDLE, 'videos')

    categories = get_categories()
    for (name, display, pic) in categories:
        list_item = xbmcgui.ListItem(label=display, offscreen=True)

        list_item.setArt({'thumb': pic,
                          'icon': pic,
                          'fanart': pic})

        vid_info = list_item.getVideoInfoTag()
        vid_info.setTitle(display)
        vid_info.setGenres([name])
        vid_info.setMediaType('video')

        if name == "search":
            url = get_url(action='search')
        else:
            url = get_url(action='listing', category=name)
        is_folder = True
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_HANDLE)

def play_video(video):
    info = extract_info(video)
    url = extract_manifest_url_from_info(info)

    adaptive_type = False

    if url:
        adaptive_type = get_adaptive_type_from_url(url)

    if not url or not check_if_kodi_supports_manifest(adaptive_type):
        err_msg = localize(33000)
        log(err_msg)
        show_info(err_msg)
        raise Exception(err_msg)

    list_item = xbmcgui.ListItem(info['title'], path=url)

    list_item.setProperty("IsPlayable","true")
    
    if adaptive_type:
        list_item.setProperty('inputstream', 'inputstream.adaptive')
        list_item.setProperty('inputstream.adaptive.manifest_type', adaptive_type)

    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=list_item)

def search_videos():
    keyword = xbmcgui.Dialog().input("Search")

    xbmcplugin.setContent(_HANDLE, 'videos')

    videos = tver.search_episodes(keyword)
    for video in videos:
        label = video['name']
        list_item = xbmcgui.ListItem(label=label, offscreen=True)

        vid_info = list_item.getVideoInfoTag()
        vid_info.setTitle(label)
        vid_info.setTvShowTitle(video['series'])
        vid_info.setMediaType('video')

        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')

        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)

    xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.endOfDirectory(_HANDLE)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        action = params['action']
        if action == 'listing':
            list_videos(params['category'])
        elif action == 'search':
            search_videos()
        elif action == 'play':
            play_video(params['video'])
        elif action == 'mylist':
            MyList().add(params['category'], params['series'], params['series_title'])
        elif action == 'delist':
            MyList().remove(params['series'])
            refresh()
        elif action == 'thumbnails':
            clear_thumbnails()
        elif action == 'favourites':
            Favourites().list()
        else:
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        list_categories()

if __name__ == '__main__':
    router(sys.argv[2][1:])
