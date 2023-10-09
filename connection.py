# api_connection.py
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from flask import url_for, redirect
import pandas as pd

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', '.env'))
load_dotenv(dotenv_path)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def create_spotify_oauth(redirect_uri):
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-library-read'
    )

def get_token(redirect_uri):
    sp_oauth = create_spotify_oauth(redirect_uri=redirect_uri)
    token_info = sp_oauth.get_access_token()
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
 
    if is_expired:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
 
    return token_info