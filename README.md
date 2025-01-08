# plugin.video.tver modified by toskaw
# Tver プラグイン toskaw 改造版

## 改造点
- [x] タイトルでの並べ替えを追加
- [x] カテゴリーなどのリストを番組名でフォルダー化
- [x] すべて、未視聴、視聴済みで絞り込み

## Changes
- [x] add sort method by title
- [x] Category list grouping by TV series
- [x] add filter method all, unwatched, watched

## Sxreenshots
<img src="https://github.com/toskaw/plugin.video.tver/blob/master/screenshots/sort.png?raw=true" alt="sort by title" width="400"/> <img src="https://github.com/toskaw/plugin.video.tver/blob/master/screenshots/grouping.png?raw=true" alt="grouping" width="400"/>
<img src="https://github.com/toskaw/plugin.video.tver/blob/master/screenshots/filter.png?raw=true" alt="filter" width="400"/>


# plugin.video.tver
An opinionated [Kodi](https://kodi.tv) video addon for accessing [TVer.jp](https://tver.jp/) VODs

<img src="https://github.com/kuriho/plugin.video.tver/blob/master/icon.png?raw=true" alt="drawing" width="200"/>

## Features
- [x] extracts TVer.jp video and audio streams using [yt-dlp](https://github.com/yt-dlp/yt-dlp) 
- [x] addon internal favourites
- [x] continue watching list

## Installation
Download the [latest release](https://github.com/kuriho/plugin.video.tver/releases) and follow the instructions provided by the official Kodi wiki [How to install from a ZIP file](https://kodi.wiki/view/Add-on_manager#How_to_install_from_a_ZIP_file)

Successfully tested on [LibreElec 11.0.5](https://libreelec.tv/2024/01/14/libreelec-nexus-11-0-5/). Should be compatible with every platform and every version of Kodi supporting Python 3.9+ (19.0+). As of Kodi 21.1(Omega) the windows version still comes bundled and build with cPython 3.8. Either use [v0.3.8](https://github.com/kuriho/plugin.video.tver/releases/tag/v0.3.8) or manually bump your Kodi's Python version.

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
