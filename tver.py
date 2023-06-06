import requests
from cache import Cache
from watcher import Watcher
from utils import get_random_ua, strip_or_none, get_custom_img_path, find_episode, localize
from urllib.parse import parse_qsl

URL_TOKEN_SERVICE = 'https://platform-api.tver.jp/v2/api/platform_users/browser/create'
URL_TAG_SEARCH_WS = 'https://platform-api.tver.jp/service/api/v1/callTagSearch/{}'
URL_LIST_EPISODES =  URL_TAG_SEARCH_WS + '?platform_uid={}&platform_token={}'
URL_VIDEO_WEBSITE = 'https://tver.jp/{}s/{}'
URL_VIDEO_PICTURE = 'https://statics.tver.jp/images/content/thumbnail/{}/small/{}.jpg'
URL_VIDEO_CONTENT = 'https://statics.tver.jp/content/{}/{}.json'

CATEGORIES = [
        ("variety",localize(30005), get_custom_img_path("variety.jpg")),
        ("drama",localize(30006), get_custom_img_path("drama.jpg")),
        ("anime",localize(30007), get_custom_img_path("anime.jpg")),
        ("documentary",localize(30008), get_custom_img_path("documentary.jpg")),
        ("sports",localize(30009), get_custom_img_path("sports.jpg")),
    ]

def get_categories():
    return CATEGORIES

def fetch_api_token():
    resp = requests.post(URL_TOKEN_SERVICE, data=b'device_type=pc', headers={
                'user-agent': get_random_ua(),
                'Origin': 'https://s.tver.jp',
                'Referer': 'https://s.tver.jp/',
                'Content-Type': 'application/x-www-form-urlencoded',
            }, timeout=10)
    
    json_token = resp.json()

    uid = json_token['result']['platform_uid']
    token = json_token['result']['platform_token']
    return (uid,token)

def fetch_episodes(category):
    cache = Cache()

    cached_episodes = cache.get(category)
    if cached_episodes != None:
        return cached_episodes
    
    (uid, token) = fetch_api_token()
    resp = requests.get(URL_LIST_EPISODES.format(category, uid, token), headers={'x-tver-platform-type': 'web'}, timeout=10)
    data = resp.json()

    cache.insert(category, data)
    return data

def get_episodes(category):
    json_episodes = fetch_episodes(category)

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

def get_watching_episodes():
    episodes = []

    watching = Watcher().select()

    if watching:
        full_cache = Cache().get_all()

        for row in watching:
            file = row[0]
            params = dict(parse_qsl(file))
            tver_url = params['video']
            video_id = str(tver_url).split('/')[-1]

            episode = find_episode(full_cache, video_id)
            if episode:
                label = ' '.join(filter(None, [strip_or_none(episode['seriesTitle']), strip_or_none(episode['title'])]))
                episodes.append({ 'name': label,
                                  'series': None, 
                                  'thumb': URL_VIDEO_PICTURE.format('episode', video_id),
                                  'video': tver_url, 
                                  'genre': None })
            else:
                #video got pulled by tver
                episodes.append({ 'name': video_id,
                                  'series': None, 
                                  'thumb': URL_VIDEO_PICTURE.format('episode', video_id),
                                  'video': tver_url, 
                                  'genre': None })
    return episodes
