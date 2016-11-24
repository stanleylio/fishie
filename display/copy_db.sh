#!/bin/bash

# Clone the database sent in by the field base station
#
# One of these days I'm gonna switch the whole thing to MySQL or some other managed database.
#
# The .backup command in sqlite3 append to instead of replace the data in the target database (if exist)
# ... but if I use .clone then the clone loses the group-write permission.
# ... I'm still not convinced that the Linux permission system is a good feature.

echo "PoH"

SRC_DB="/home/nuc/data/base-003/storage/sensor_data.db"
#SRC_DB="/home/nuc/data/base-004/storage/sensor_data.db"
TGT_DIR="/home/nuc/node/www/poh/storage"

rm -f $TGT_DIR/sensor_data.db
rm -f $TGT_DIR/sensor_data.db-shm
rm -f $TGT_DIR/sensor_data.db-wal

# http://stackoverflow.com/questions/25675314/how-to-backup-sqlite-database
#sqlite3 /home/nuc/data/base-003/storage/sensor_data.db ".backup /home/nuc/node/storage/sensor_data.db"
#sqlite3 $SRC_DB ".backup "$TGT_DIR"/sensor_data.db"
sqlite3 $SRC_DB ".clone "$TGT_DIR"/sensor_data.db"

# change permissions
chmod g+w $TGT_DIR/sensor_data.db
if [ -e $TGT_DIR/sensor_data.db-shm ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-shm
fi
if [ -e $TGT_DIR/sensor_data.db-wal ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-wal
fi


# - - - - -
# Coconut Island tank test
# - - - - -
echo "Coconut Island"

SRC_DB="/home/nuc/data/base-002/storage/sensor_data.db"
TGT_DIR="/home/nuc/node/www/coconut/storage"

rm -f $TGT_DIR/sensor_data.db
rm -f $TGT_DIR/sensor_data.db-shm
rm -f $TGT_DIR/sensor_data.db-wal

sqlite3 $SRC_DB ".clone "$TGT_DIR"/sensor_data.db"

# change permissions
chmod g+w $TGT_DIR/sensor_data.db
if [ -e $TGT_DIR/sensor_data.db-shm ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-shm
fi
if [ -e $TGT_DIR/sensor_data.db-wal ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-wal
fi


# - - - - -
# Hollie's
# - - - - -
echo "Hollie's"

SRC_DB="/home/nuc/data/htank/storage/sensor_data.db"
TGT_DIR="/home/nuc/node/www/htank/storage"

rm -f $TGT_DIR/sensor_data.db
rm -f $TGT_DIR/sensor_data.db-shm
rm -f $TGT_DIR/sensor_data.db-wal

sqlite3 $SRC_DB ".clone "$TGT_DIR"/sensor_data.db"

# change permissions
chmod g+w $TGT_DIR/sensor_data.db
if [ -e $TGT_DIR/sensor_data.db-shm ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-shm
fi
if [ -e $TGT_DIR/sensor_data.db-wal ]
	then
		chmod g+w $TGT_DIR/sensor_data.db-wal
fi






