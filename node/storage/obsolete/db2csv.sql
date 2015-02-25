

--this creates a CSV where all the timestamps are human readable strings rather than a POSIX timestamp that Python can use.
--use db2csv.py if the output CSV is to be used by Python.


.headers on
.mode csv
.output sensor_data.csv
SELECT * FROM Samples;
.output stdout
