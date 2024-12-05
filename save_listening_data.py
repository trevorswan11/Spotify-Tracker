import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sqlite3
import os
from dotenv import load_dotenv

# Load the environment variables from .env
load_dotenv()

# Access Spotify credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8888/callback'

# Scopes required for accessing recently played tracks
SCOPE = 'user-read-recently-played'

# SQLite database file
DB_FILE = 'song_history.db'

def setup_database():
    """Initialize the SQLite database and create the required table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tables should include all relevant song info, but there should not be duplicate time entires
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

    # Apply the changes and disconnect
    conn.commit()
    conn.close()

def fetch_recent_tracks(spotify: spotipy.Spotify):
    """Fetch recently played tracks from Spotify."""
    results = spotify.current_user_recently_played(limit=50)
    tracks = []

    for item in results['items']:
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
    """Save a list of tracks to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for track in tracks:
        try:
            cursor.execute('''
                INSERT INTO songs (track_name, artist, album, played_at, duration_ms)
                VALUES (?, ?, ?, ?, ?)
            ''', (track['track_name'], track['artist'], track['album'], track['played_at'], track['duration_ms']))
        except sqlite3.IntegrityError:
            # Skip duplicates (constraint on played_at)
            pass

    conn.commit()
    conn.close()

def main():
    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

    # Ensure the database is ready
    setup_database()

    # Fetch and save tracks
    tracks = fetch_recent_tracks(sp)
    save_tracks_to_db(tracks)


if __name__ == '__main__':
    main()