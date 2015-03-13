
REM dump the database to a sql file, then reconstruct a new database again
REM for some reason database modified in BBB is not recognized by Windows. Some version mismatch I guess.

del sensor_data.db.old
del tmp.sql

sqlite3 sensor_data.db < conv.sql
rename sensor_data.db sensor_data.db.old
sqlite3 sensor_data.db < tmp.sql

del sensor_data.db.old
del tmp.sql
