#!/bin/bash

# http://linuxconfig.org/passwordless-ssh
#ssh-keygen
#ssh-copy-id hlio@uhunix.hawaii.edu
#ls ~/.ssh/id_rsa.pub
#ssh hlio@uhunix.hawaii.edu

# the parent directory must exist on the server first as rsync won't recreate the entire dir structure

date

# glazerlab-i7nuc
BENCHTEST_DIR="nuc@128.171.153.115:/home/nuc/data/$(hostname)"

# path of the rsync binary on the remote machine
# glazerlab-i7nuc
REMOTE_RSYNC_PATH=/usr/bin/rsync

echo "upload database"
#rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./storage/sensor_data* $BENCHTEST_DIR/storage/
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./storage/sensor_data.db* $BENCHTEST_DIR/storage/

echo "upload log"
#date > $HOME/node/log/upload.log
rsync -avzhe ssh --rsync-path=$REMOTE_RSYNC_PATH --progress ./log/* $BENCHTEST_DIR/log/
