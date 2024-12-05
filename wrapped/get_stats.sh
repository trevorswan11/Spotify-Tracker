#!/bin/bash
cd /Users/Trevor/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Trevor/Projects/Spotify-Tracker
source myenv/bin/activate
cd /Users/Trevor/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Trevor/Projects/Spotify-Tracker/wrapped
YEAR=$(date +"%Y")
python get_spotify_stats.py $YEAR > "mywrapped/${YEAR}_spotify_wrapped.md"
deactivate