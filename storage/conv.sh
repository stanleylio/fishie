#!/bin/bash

echo "delete temporary files (if any)"
rm sensor_data.db.old
rm tmp.sql

echo "dump to .sql"
sqlite3 sensor_data.db < conv.sql
mv sensor_data.db sensor_data.db.old
echo "rebuild .db"
sqlite3 sensor_data.db < tmp.sql

echo "delete temporary files"
rm sensor_data.db.old
rm tmp.sql
