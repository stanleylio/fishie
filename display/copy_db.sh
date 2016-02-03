#!/bin/bash

# Clone the database sent in by the field base station
#
# The .backup command in sqlite3 append to instead of replace the data in the target database (if exist)
# ... but if I use .clone then the clone loses the group-write permission.
# ... I'm still not convinced that the Linux permission system is a good feature.

SRC_DB="/home/nuc/data/base-003/storage/sensor_data.db"
TGT_DIR="/home/nuc/node/www/poh/storage"

rm -f $TGT_DIR/sensor_data.db
rm -f $TGT_DIR/sensor_data.db-shm
rm -f $TGT_DIR/sensor_data.db-wal

# http://stackoverflow.com/questions/25675314/how-to-backup-sqlite-database
#sqlite3 /home/nuc/data/base-003/storage/sensor_data.db ".backup /home/nuc/node/storage/sensor_data.db"
#sqlite3 $SRC_DB ".backup "$TGT_DIR"/sensor_data.db"
sqlite3 $SRC_DB ".clone "$TGT_DIR"/sensor_data.db"

chmod g+w $TGT_DIR/sensor_data.db
chmod g+w $TGT_DIR/sensor_data.db-shm
chmod g+w $TGT_DIR/sensor_data.db-wal
