#!/usr/bin/python3

import sys
from spoti import SpotifyAPI
from youtube import YoutubeAPI

client_id = '4979459f9eae4d6b9bcc7b626f19b03b'
client_secret = 'd594287114de46798243f83230f385db'

yt = YoutubeAPI()
sp = SpotifyAPI(client_id, client_secret)

sp_playlist = sp.get_playlist_sa(sys.argv[1])
yt_playlist = yt.create_playlist(sys.argv[2])

for x in sp_playlist:
    res = yt.search(f"{x} - Lyrics")
    #print(res)
    for y in res['items']:
        if 'lyrics' in y['snippet']['title'] or 'Lyrics' in y['snippet']['title'] or 'Letra' in y['snippet']['title']:
            print(y['id'])
            yt.add_song_to_playlist(y['id']['videoId'], yt_playlist["id"])
            continue
