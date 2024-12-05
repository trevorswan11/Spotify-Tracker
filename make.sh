#!/bin/bash
echo "Creating necessary project files and entering venv..."
python3 -m venv myenv
source myenv/bin/activate
touch song_history.db
touch .env
echo SPOTIFY_CLIENT_ID="your_client_id // TODO" > .env
echo SPOTIFY_CLIENT_SECRET="your_client_secret // TODO" > .env
cd wrapped
mkdir history
mkdir mywrapped
echo "All necessary project files created, use deactivate to leave venv..."