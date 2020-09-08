#!/usr/bin/python3

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

class YoutubeAPI(object):
    yt = None

    def __init__(self):
        CLIENT_SECRETS_FILE = "client_secret.json"
        MISSING_CLIENT_SECRETS_MESSAGE = os.path.abspath(os.path.join(os.path.dirname(__file__),CLIENT_SECRETS_FILE)) 
        YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"

        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
        scope=YOUTUBE_READ_WRITE_SCOPE)
        
        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()
        
        if credentials is None or credentials.invalid:
            print("qloq")
            flags = argparser.parse_args()
            credentials = run_flow(flow, storage, flags)
        
        self.yt = build('youtube', 'v3',
        http=credentials.authorize(httplib2.Http()))

    def search(self, q):
        r = self.yt.search().list(q=q, part='snippet', type='video', maxResults=1)
        return r.execute()

    def create_playlist(self, name, p_description='No description'):
        part = 'snippet,status'
        body = {
                "snippet" : {
                        "title" : name,
                        "description" : p_description
                    },
                "status" : { "privacyStatus" : "public"}
                }
        r = self.yt.playlists().insert(part=part, body=body).execute()
        return r

    def add_song_to_playlist(self, song_id, playlist_id):
        r = self.yt.playlistItems().insert(
                    part = 'snippet',
                    body = {
                            "snippet" : {
                                    "playlistId" : playlist_id,
                                    "resourceId" : {
                                            "kind" : "youtube#video",
                                            "videoId" : song_id
                                        }
                                }
                        }
                    ).execute()

