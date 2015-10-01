#!/bin/bash

sqlite3 sensor_data.db < db2csv.sql
#echo db2csv.sql | sqlite3 sensor_data.db
