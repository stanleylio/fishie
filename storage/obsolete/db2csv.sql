

--this creates a CSV where all the timestamps are human readable strings rather than a POSIX timestamp that Python can use.
--use db2csv.py if the output CSV is to be used by Python.


.headers on

.mode csv
.output sensor_data_node_001.csv
SELECT * FROM node_001;
.output stdout

.mode csv
.output sensor_data_node_002.csv
SELECT * FROM node_002;
.output stdout

.mode csv
.output sensor_data_node_003.csv
SELECT * FROM node_003;
.output stdout

.mode csv
.output sensor_data_node_004.csv
SELECT * FROM node_004;
.output stdout

