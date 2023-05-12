import os
from dotenv import load_dotenv
from auth import Auth
import json
import playlist

load_dotenv()


'''
TODO
add json dictionary of access tokens
implement token refreshing
'''

def main():
    client_id = os.getenv("CLIENT_ID")
    secret = os.getenv("CLIENT_SECRET")
    response_type = 'code'
    redirect_uri = 'https://localhost/callback'
    scope = 'playlist-modify-public playlist-modify-private user-read-playback-state user-modify-playback-state'

    auth = Auth(client_id, secret, response_type, redirect_uri, scope)

    header = auth.get_auth_header()
    uris = ['4wEuNvb7oG8oZYrZPZ9rPr']
    playlist_uri = '3EeTvYJ7iVn8aMPtLxavbI'
    pos = 0

    playlist.shuffler(playlist_id=playlist_uri, header=header)
    
main()