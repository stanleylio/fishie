#!/bin/bash

# CSV export is slow, so I took only the website upload part so that I can schedule it to run more frequently.
# --SL

scp -r ./* glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
