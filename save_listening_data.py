import requests
import sqlite3
import os
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

# Access Spotify credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
REDIRECT_URI = 'http://localhost:8888/callback'

API_BASE_URL = 'https://api.spotify.com/v1/'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Scopes required for accessing recently played tracks
SCOPE = 'user-read-recently-played'

# SQLite database file
DB_FILE = 'song_history.db'

def setup_database():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_name TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT NOT NULL,
            played_at TEXT UNIQUE NOT NULL,
            duration_ms INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def refresh_access_token():
    """Get a new access token using the refresh token."""
    response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )
    response.raise_for_status()
    token_info = response.json()
    return token_info['access_token']

def fetch_recent_tracks(access_token):
    """Fetch recently played tracks from Spotify."""
    url = f'{API_BASE_URL}me/player/recently-played?limit=50'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()
    tracks = []
    for item in data['items']:
        track = item['track']
        played_at = item['played_at']
        tracks.append({
            'track_name': track['name'],
            'artist': ', '.join(artist['name'] for artist in track['artists']),
            'album': track['album']['name'],
            'played_at': played_at,
            'duration_ms': track['duration_ms']
        })
    return tracks

def save_tracks_to_db(tracks):
    """Save tracks to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for track in tracks:
        try:
            cursor.execute('''
                INSERT INTO songs (track_name, artist, album, played_at, duration_ms)
                VALUES (?, ?, ?, ?, ?)
            ''', (track['track_name'], track['artist'], track['album'], track['played_at'], track['duration_ms']))
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

def main():
    """Main function to fetch and save tracks."""

    # Ensure database is ready
    setup_database()

    # Refresh token and fetch tracks
    access_token = refresh_access_token()
    tracks = fetch_recent_tracks(access_token)
    if tracks:
        save_tracks_to_db(tracks)

if __name__ == '__main__':
    main()