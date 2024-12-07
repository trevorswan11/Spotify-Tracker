#!/bin/bash
# Functions
model_service() {
    local file="$1"
    echo "[Unit]" >> "$file"
    echo "Description=Description to match timer" >> "$file"
    echo "After=network.target" >> "$file"
    echo "" >> "$file"
    echo "[Service]" >> "$file"
    echo "Type=oneshot" >> "$file"
    echo "ExecStart=/bin/bash path_to_script" >> "$file"
    echo "User=<your user>" >> "$file"
    echo "Group=<your group> # Sometimes the same as your user" >> "$file"
    echo "" >> "$file"
    echo "[Install]" >> "$file"
    echo "WantedBy=multi-user.target" >> "$file"
}

model_timer() {
    local file="$1"
    echo "[Unit]" >> "$file"
    echo "Description=Description to match service" >> "$file"
    echo "" >> "$file"
    echo "[Service]" >> "$file"
    echo "OnCalendar=DayOfWeek Year-Month-Day Hour:Minute:Second" >> "$file"
    echo "Persistent=true" >> "$file"
    echo "" >> "$file"
    echo "[Install]" >> "$file"
    echo "WantedBy=timers.target" >> "$file"
}

# Initial required files and folders
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
mkdir sys
mkdir logs

# backup.sh
echo "#!/bin/bash" >> backup.sh
echo "TRACKER_PATH=path to spotify-tracker" >> backup.sh
echo "BACKUP_PATH=path to backup location" >> backup.sh
echo "DATE=$(date +%F_%H-%M-%S)" >> backup.sh
echo "TRACKER_BACKUP_NAME=desired name of backup file" >> backup.sh
echo "" >> backup.sh
echo "echo "$(date): Backup Started" >> $BACKUP_PATH/backup.log" >> backup.sh
echo "tar -czf "$BACKUP_PATH/$TRACKER_BACKUP_NAME" -C "$TRACKER_PATH" --exclude='.git' ." >> backup.sh
echo "echo "$(date): Backup Finished" >> $BACKUP_PATH/backup.log" >> backup.sh
echo "echo "" >> $BACKUP_PATH/backup.log" >> backup.sh
echo "" >> backup.sh
echo "cd $TRACKER_PATH/logs" >> backup.sh
echo "rm save_data.log" >> backup.sh
echo "touch save_data.log" >> backup.sh

# run_save_data.sh
echo "#!/bin/bash" >> run_save_data.sh
echo "current_date=$(date +"%m-%d")" >> run_save_data.sh
echo "if [ "$current_date" == "01-01" ]; then" >> run_save_data.sh
echo "  exit 0" >> run_save_data.sh
echo "fi" >> run_save_data.sh
echo "" >> run_save_data.sh
echo "DIRECTORY=path to spotify tracker" >> run_save_data.sh
echo "cd $DIRECTORY" >> run_save_data.sh
echo "source myenv/bin/activate" >> run_save_data.sh
echo "python save_listening_data.py" >> run_save_data.sh
echo "echo "Saved at $(date)" >> logs/save_data.log" >> run_save_data.sh
echo "deactivate" >> run_save_data.sh


# Sys directory files
cd sys
echo "You can use .service and .timer files to automate. Complete/Write your own implementations for backup.sh, run_save_data.sh, new_cylce.sh, and wrapped.sh" >> HELP.md
echo "" >> HELP.md
echo "Note: You can also automate using cronjob :)" >> HELP.md

touch spotify-reset.service
model_service "spotify-reset.service"
touch spotify-reset.timer
model_timer "spotify-reset.timer"

touch spotify-tracker-backup.service
model_service "spotify-tracker-backup.service"
touch spotify-tracker-backup.timer
model_timer "spotify-tracker-backup.timer"

touch spotify-save-data.service 
model_service "spotify-save-data.service"
touch spotify-save-data.timer
model_timer "spotify-save-data.timer"

# Log directory files
cd ../logs
touch save_data.log
cd ../wrapped

# new_cylce.sh
echo "#!/bin/bash" >> new_cycle.sh
echo "TRACKER_PATH=path to spotify-tracker" >> new_cycle.sh
echo "BACKUP_PATH=path to backup location" >> new_cycle.sh
echo "YEAR=$(date +"%Y")" >> new_cycle.sh
echo "TRACKER_BACKUP_NAME=desired name of backup file" >> new_cycle.sh
echo "WRAPPED="$TRACKER_PATH/wrapped"" >> new_cycle.sh
echo "" >> new_cylce.sh
echo "echo "$(date): Backup Started" >> $BACKUP_PATH/backup.log" >> new_cycle.sh
echo "tar -czf "$BACKUP_PATH/$TRACKER_BACKUP_NAME" -C "$TRACKER_PATH" --exclude='.git' ." >> new_cycle.sh
echo "echo "$(date): Backup Finished" >> $BACKUP_PATH/backup.log" >> new_cycle.sh
echo "echo "" >> $BACKUP_PATH/backup.log" >> new_cycle.sh
echo "" >> new_cycle.sh
echo "cd $TRACKER_PATH/wrapped/mywrapped" >> new_cycle.sh
echo "echo "$(date): Reset Started" >> ../reset.log" >> new_cycle.sh
echo "./wrapped.sh" >> new_cycle.sh
echo "mv $TRACKER_PATH/song_history.db ../history/${YEAR}_song_history.db" >> new_cycle.sh
echo "echo "$(date): Reset Finished" >> ../reset.log" >> new_cycle.sh
echo "echo "" >> ../reset.log" >> new_cycle.sh
echo "" >> new_cycle.sh
echo "cd $TRACKER_PATH" >> new_cycle.sh
echo "touch song_history.db" >> new_cycle.sh

mkdir history
mkdir mywrapped
cd mywrapped

# wrapped.sh
echo "#!/bin/bash" >> wrapped.sh
echo "DIRECTORY=path to spotify-tracker" >> wrapped.sh
echo "cd $DIRECTORY" >> wrapped.sh
echo "source myenv/bin/activate" >> wrapped.sh
echo "cd $DIRECTORY/wrapped/mywrapped" >> wrapped.sh
echo "YEAR=$(date +"%Y")" >> wrapped.sh
echo "python get_wrapped.py > "${YEAR}_spotify_wrapped.md"" >> wrapped.sh
echo "deactivate" >> wrapped.sh

touch reset.log
echo "All necessary project files created."


