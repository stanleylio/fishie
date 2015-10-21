#!/bin/bash

table="node_005"

sqlite3 <<!
.open sensor_data.db
.headers on
.mode csv
.output sensor_data.csv
select * from $table;
!
