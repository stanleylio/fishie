#!/bin/bash

# CSV export is slow, so I isolated the website upload part so that page upload can be scheduled more frequently.
# --SL

echo "upload webpage"
rsync -avzhe ssh --progress ./www/* glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest

echo "upload database"
rsync -avzhe ssh --progress ./storage/sensor_data.db glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest
