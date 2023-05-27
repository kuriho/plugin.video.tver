# plugin.video.tver
An opinionated [Kodi](https://kodi.tv) video addon for accessing [TVer.jp](https://tver.jp/) VODs

<img src="https://github.com/kuriho/plugin.video.tver/blob/master/icon.png?raw=true" alt="drawing" width="200"/>

## Features
- [x] extracts TVer.jp video and audio streams using [yt-dlp](https://github.com/yt-dlp/yt-dlp) 
- [x] addon internal favourites
- [x] continue watching list

## Installation
Download the [latest release](https://github.com/kuriho/plugin.video.tver/releases) and follow the instructions provided by the official Kodi wiki [How to install from a ZIP file](https://kodi.wiki/view/Add-on_manager#How_to_install_from_a_ZIP_file)

Successfully tested on [LibreElec 11.0.1](https://libreelec.tv/2023/03/24/libreelec-nexus-11-0-1/) and Windows 10/11 using [Kodi v20.1](https://kodi.tv/download/). Should be compatible with every platform and every version of Kodi supporting Python 3 (19.0+).  

## Screenshots
<img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/1.png?raw=true" alt="screenshot 1" width="400"/> <img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/2.png?raw=true" alt="screenshot 2" width="400"/>
<img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/3.png?raw=true" alt="screenshot 3" width="400"/> <img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/4.png?raw=true" alt="screenshot 4" width="400"/>

## Troubleshooting
<img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/arial.png?raw=true" alt="use arial font" width="400"/>
Q: Japanese characters aren't being displayed correctly.

A: Switch to a Arial based font. ( Settings > Interface > Skin > Fonts > Select "Arial Based" )

<img src="https://github.com/kuriho/plugin.video.tver/blob/master/screenshots/pulled.png?raw=true" alt="episode got pulled" width="400"/>
Q: An episode in my continue watching list can no longer be accessed.

A: TVer.jp sometimes pulls episodes from their website even before their set expiration date. After verifying that this particular episode is no longer available on TVer.jp all you can do is mark the episode as watched via the context menu.
