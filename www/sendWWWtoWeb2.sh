#!/bin/bash

# CSV export is slow, so I isolated the website upload part so that it can be scheduled more frequently.
# --SL

scp -r $HOME/base/www/* glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
