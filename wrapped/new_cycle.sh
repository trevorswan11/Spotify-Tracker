#!/bin/bash
TRACKER_PATH="/home/trevor/spotify-tracker"
BACKUP_PATH="/media/trevor/71B4-F53C/backups/spotify-tracker-backups/years/"
YEAR=$(date +"%Y")
TRACKER_BACKUP_NAME="spotify-tracker-wrapped-$YEAR.tar.gz"
WRAPPED="$TRACKER_PATH/wrapped"

echo "$(date): Backup Started" >> $BACKUP_PATH/backup.log
tar -czf "$BACKUP_PATH/$TRACKER_BACKUP_NAME" -C "$TRACKER_PATH" --exclude='.git' .
echo "$(date): Backup Finished" >> $BACKUP_PATH/backup.log
echo "" >> $BACKUP_PATH/backup.log

cd $TRACKER_PATH/wrapped/mywrapped
echo "$(date): Reset Started" >> ../reset.log
./wrapped.sh
mv $TRACKER_PATH/song_history.db ../history/${YEAR}_song_history.db
echo "$(date): Reset Finished" >> ../reset.log
echo "" >> ../reset.log

cd $TRACKER_PATH
touch song_history.db
