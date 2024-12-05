# Spotify Tracker
A simple app that store the most recent songs played on spotify. The data is stored in a sqlite database, and makes sure to ignore overlapping songs. For best results, run the bash script on a timer so that it updates every hour or half hour.

## Environment Variables
Please make sure you have a .env file in your folder with the following variables:

```dotenv
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

## Python Modules
Please make sure you have the following pip modules installed:

```bash
pip install spotipy
pip install sqlite3
pip install python-dotenv
```

You can also run `pip install -r requirements.txt` in this directory.

*Note: While sqlite3 is needed for this project, it may come installed with your python version. Run `python3 -m sqlite3` in your terminal to verify it is present without errors.*

## Things to Consider
- Make sure your spotify token has the correct scopes, specifically include the `user-read-recently-played` scope for your client.
- If you want to align your listening data with the standard spotify schedule, you can set up a system task to store and batch delete the database.
- I recommend storing copies of the data in a folder named `wrapped/history`, so that you can run stats on any year you'd like.
- When creating your app on [spotify's developer website](https://developer.spotify.com/), you'll be prompted for expected APIs and redirect URIs. I use `http://localhost:8888/callback` as my redirect URI, and chose `Web API` for my APIs used. These are modifiable in the future, just make sure your code reflects any changes.

## Other
- The database is stored as `song_history.db`, and is accessed by functions in the code. This must be created before the script can run.
- You can use `get_spotify_stats.py` file in the `wrapped` folder to get your current statistics.
- I recommend making a python virtual environment to run this project, but it is not required.
- When you run `save_listening_data.py` for the first time, it should open a website asking for access to your spotify account. After you press agree, the code should save your data to `song_history.db`.

---

*This was inspired by [@lizstip](https://www.tiktok.com/@lizstip?_t=8rxwoJUhOo6&_r=1) on TikTok*
