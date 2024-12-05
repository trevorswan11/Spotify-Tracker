# Spotify Tracker
A simple app that store the most recent songs played on spotify. The data is stored in a sqlite database, and makes sure to ignore overlapping songs. For best results, run the bash script on a timer so that it updates every hour or half hour.

## Environment Variables
Please make sure you have a .env file in your folder with the following variables:

```dotenv
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REFRESH_TOKEN=your_refresh_token
```

I don't think you need the `SPOTIFY_REFRESH_TOKEN`, but it may be useful for future scaling.

## Python Modules
Please make sure you have the following pip modules installed:

```bash
pip install spotipy
pip install sqlite3
pip install python-dotenv
```

## Things to Consider
- Make sure your spotify token has the correct scopes, specifically include the `user-read-recently-played` scope for your client.
- If you want to align your listening data with the standard spotify schedule, you can set up a system task to store and batch delete the database.
- I recommend storing copies of the data in a folder named `wrapped`, so that you can run stats on any year you'd like.

## Other
Also, the database is stored as `song_history.db`, and is accessed by functions in the code. You can use `get_spotify_stats.py` file in the `wrapped` folder to get your current statistics.

---

*This was inspired by @lizstip on TikTok*
