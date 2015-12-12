#!/bin/bash

#logging_dir="/root/projects/logging"
#cd $logging_dir/storage

sqlite3 sensor_data.db < backup.sql

#gzip -f sensor_data_backup_daily.db
tar cvzf sensor_data_daily.tar.gz sensor_data.db.bak sensor_data.db.sql

rm sensor_data.db.bak
rm sensor_data.db.sql
