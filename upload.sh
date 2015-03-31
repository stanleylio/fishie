#!/bin/bash

BENCHTEST_DIR="glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest"

echo "upload webpage"
rsync -avzhe ssh --progress ./www/* $BENCHTEST_DIR

echo "upload database"
rsync -avzhe ssh --progress ./storage/sensor_data.db $BENCHTEST_DIR
rsync -avzhe ssh --progress ./storage/sensor_data.db-shm $BENCHTEST_DIR
rsync -avzhe ssh --progress ./storage/sensor_data.db-wal $BENCHTEST_DIR
