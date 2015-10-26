#!/bin/bash

# http://linuxconfig.org/passwordless-ssh
#ssh-keygen
#ssh-copy-id hlio@uhunix.hawaii.edu
#ls ~/.ssh/id_rsa.pub
#ssh hlio@uhunix.hawaii.edu

# the parent directory must exist on the server first as rsync won't recreate the entire dir structure

#BENCHTEST_DIR="glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/PoH"
#BENCHTEST_DIR="glazer@128.171.151.240:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/PoH"
# UH UNIX
#BENCHTEST_DIR="hlio@uhunix.hawaii.edu:/home04/h/hlio/public_html/base-003"
#BENCHTEST_DIR="hlio@128.171.24.197:/home04/h/hlio/public_html/$(hostname)"
BENCHTEST_DIR="nuc@128.171.153.115:/home/nuc/data/$(hostname)"

# path of the rsync binary on the remote machine
# UH UNIX
#REMOTE_RSYNC_PATH=/usr/local/bin/rsync
# glazerlab-i7nuc
REMOTE_RSYNC_PATH=/usr/bin/rsync

echo "upload database"
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./storage/sensor_data.db* $BENCHTEST_DIR/storage/

echo "upload webpage"
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./www/* $BENCHTEST_DIR/www/

echo "upload log"
tail ./log/raw.txt -n 100 > ./log/tail.txt
tail ./log/tsraw.txt -n 100 > ./log/tstail.txt
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./log/* $BENCHTEST_DIR/log/



# = = = = =
exit 0
# = = = = =



#BENCHTEST_DIR="glazer@imina.soest.hawaii.edu:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/PoH"
BENCHTEST_DIR="glazer@128.171.151.240:/export/imina2/httpd/htdocs/oceanography/glazer/Brian_T._Glazer/research/DataLoggers/PoH/$(hostname)"

echo "upload database"
rsync -avzhe ssh --progress ./storage/sensor_data.db* $BENCHTEST_DIR/storage/

echo "upload webpage"
rsync -avzhe ssh --progress ./www/* $BENCHTEST_DIR/www/

echo "upload log"
tail ./log/raw.txt -n 100 > ./log/tail.txt
rsync -avzhe ssh --progress ./log/* $BENCHTEST_DIR/log/

