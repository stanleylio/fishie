#!/bin/bash

#@glazer
#03 March 2015

clear

#these commands copy the node www directories to Glazer's web site on imina;
#this function is dependent upon RSA pairing between local and host machines
#can call this script from crontab to automate

# why not do this instead? --SL
#scp -r ./* glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/

#copy over directories full of plots in png format
scp -r ./node_001/ glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp -r ./node_002/ glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp -r ./node_003/ glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp -r ./node_004/ glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/

#copy over web pages of the plots
scp ./node_001.html glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp ./node_002.html glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp ./node_003.html glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/
scp ./node_004.html glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/

#generate node csv files from database
cd /root/base/storage/ && /bin/bash gen_csv4www.sh

#copy over csv files of the nodes
scp /root/base/storage/sensor_data_node_001.csv glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/csv/
scp /root/base/storage/sensor_data_node_002.csv glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/csv/
scp /root/base/storage/sensor_data_node_003.csv glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/csv/
scp /root/base/storage/sensor_data_node_004.csv glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/benchtest/csv/
