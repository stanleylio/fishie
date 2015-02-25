#!/bin/bash

#logging_dir="/root/projects/logging"
#cd $logging_dir/storage

sqlite3 sensor_data.db < backup.sql

#gzip -f sensor_data_backup_daily.db
tar cvzf sensor_data_weekly.tar.gz sensor_data.db.bak sensor_data.db.sql

rm sensor_data.db.bak
rm sensor_data.db.sql

# need to check the memory usage of db2csv.py. when the database get large
# later, might need to do an online read instead of reading the whole thing
# in memory first
#python db2csv.py
#gzip -f sensor_data.csv
