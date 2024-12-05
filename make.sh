#!/bin/bash
echo "Creating necessary project files..."
python3 -m venv myenv
source myenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
touch song_history.db
touch .env
echo SPOTIFY_CLIENT_ID="your_client_id // TODO" >> .env
echo SPOTIFY_CLIENT_SECRET="your_client_secret // TODO" >> .env
echo SPOTIFY_REFRESH_TOKEN="your_refresh_token" // TODO >> .env
cd wrapped
mkdir history
# mkdir mywrapped # Only needed if running a shell script to save data to this folder
echo "All necessary project files created."