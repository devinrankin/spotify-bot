import json
import re
from dotenv import load_dotenv
import os
import base64
from requests import get, post
import discord
from spotipy.oauth2 import SpotifyOAuth
import spotipy

'''
TO-DO:
    create timed database
    learn spotify get/post for a better understanding
'''

# Discord bot initialization
client = discord.Client(intents=discord.Intents.all())

# Load .env file
load_dotenv()

scope = 'playlist-modify-public'
username = 'staticccfwa'
playlist_id = '5c5FItVsMQcDwO7LmUhoBw'

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'https://localhost:8000/callback'

token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token);


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Discord event listener for songs linked in chat
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content
    author = message.author

    if match := re.match(r'https://open.spotify.com/track/(.*)\?', content):
        track_uri = match.groups()[0]
        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=[track_uri])

client.run(os.getenv('BOT_TOKEN'))
