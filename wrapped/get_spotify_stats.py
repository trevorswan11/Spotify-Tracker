import sqlite3
from pathlib import Path
from collections import Counter
from datetime import datetime

# SQLite database file
DB_FILE = 'song_history.db'

def get_total_minutes_listened():
    """Calculate the total minutes listened based on track duration."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(duration_ms) FROM songs')
    
    # Handle case where no data exists
    total_duration_ms = cursor.fetchone()[0] or 0
    conn.close()

    # Convert milliseconds to minutes
    total_minutes = total_duration_ms / 1000 / 60
    return total_minutes

def get_total_songs():
    """Get the total number of unique songs in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM songs')
    total_songs = cursor.fetchone()[0]
    conn.close()
    return total_songs

def get_top_songs(limit=5):
    """Get the top N most popular songs."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT track_name, COUNT(*) AS play_count FROM songs GROUP BY track_name ORDER BY play_count DESC LIMIT ?', (limit,))
    top_songs = cursor.fetchall()
    conn.close()
    return top_songs

def get_top_artists(limit=5):
    """Get the top N most popular artists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT artist FROM songs')
    artists = [row[0] for row in cursor.fetchall()]
    conn.close()

    # Count occurrences of each artist
    artist_counts = Counter(artist for artist_list in artists for artist in artist_list.split(', '))
    return artist_counts.most_common(limit)

def main(year: str):
    print(f"# Your {year} Spotify Wrapped!")
    print('Compiled with the help of Spotify\'s API and the spotipy module.\n')
    
    # Total number of songs
    total_songs = get_total_songs()
    print('## Unique Songs')
    print(f"You listened to {total_songs} unique songs this year!\n")

    # Total minutes listened
    total_minutes = get_total_minutes_listened()
    print('## Minutes Listened')
    print(f"This year, you listened to {total_minutes:.2f} minutes of music!\n")

    # Top 5 most popular songs
    print('## Your Top 5 Songs')
    for i, (track_name, play_count) in enumerate(get_top_songs(), start=1):
        print(f"{i}. {track_name} - {play_count} plays")
    print()

    # Top 5 most popular artists
    print('## Your Top 5 Songs')
    for i, (artist, play_count) in enumerate(get_top_artists(), start=1):
        print(f"{i}. {artist} - {play_count} plays")
    
    # Thank you
    if (year is not None):
        print('\n## What a Year!')
        print('Thanks for using my bootleg spotify wrapped, be sure to check out the official on [Spotify\'s website](https://www.spotify.com/us/wrapped/)!')

if __name__ == '__main__':
    # Check if the user wants to query an older database
    which_year = None
    doOlder = ['y', 'yes']
    older = input("Do you want to query an old db (y/n): ")
    
    try:
        # Check the users input to proceed
        if older.lower() in doOlder:
            which_year = input("Which year would you like to query: ")
            DB_FILE = f"history/{which_year}_{DB_FILE}"
        else:
            DB_FILE = f"../{DB_FILE}"
        
        # Check if the requested DB exists
        if not Path(DB_FILE).exists(): 
            raise FileNotFoundError("Database not found with specified path.")
    except:
        DB_FILE = f"../{DB_FILE}"
    main(datetime.now().year if which_year is None else which_year)